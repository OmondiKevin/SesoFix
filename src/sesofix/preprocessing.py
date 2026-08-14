"""
Preprocessing, Canonical Formatting, and Leakage-Free Splitting for SesoFix.
Enforces strict document grouping, 0% synthetic data in val/test, and complete provenance tracking.
"""

import os
import re
import hashlib
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
import pandas as pd

from .rules import SesothoRuleEngine


@dataclass
class CanonicalExample:
    """Canonical representation of a SesoFix training or evaluation example."""
    example_id: str
    source_text: str
    target_text: str
    source_type: str        # evidence label, not a claim of linguistic correctness
    source_dataset: str     # 'DS01_AUTSHUMATO' | 'DS02_NCHLT_ST' | 'DS03_CV_VERIFY'
    document_id: str        # Grouping ID to prevent document-level leakage
    is_synthetic: bool
    notes: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


def normalize_sesotho_text(text: str) -> str:
    """Apply Unicode NFC, whitespace cleanup, and typographic quote mapping.

    This view is for matching and model input. Raw provider and human text must
    be retained separately in provenance artifacts.
    """
    if not text:
        return ""
    # Normalize spaces and tabs
    cleaned = unicodedata.normalize("NFC", str(text))
    cleaned = re.sub(r"[ \t]+", " ", cleaned.strip())
    # Normalize quotes
    cleaned = cleaned.replace("“", "\"").replace("”", "\"").replace("‘", "'").replace("’", "'")
    return cleaned


def load_common_voice_verification(xlsx_path: str) -> Tuple[List[CanonicalExample], List[CanonicalExample]]:
    """
    Parses Southern Sesotho Sentence Verification Excel workbook.
    Returns:
        (legacy_single_annotator_pairs, unannotated_sa_sentences)

    The returned 74 legacy pairs were exposed during rule development and are
    not eligible for confirmatory evaluation.
    """
    if not os.path.exists(xlsx_path):
        raise FileNotFoundError(f"Verification workbook not found at: {xlsx_path}")

    with zipfile.ZipFile(xlsx_path, 'r') as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in tree:
                t_elem = si.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                strings.append(''.join([t.text for t in t_elem if t.text]))

        stree = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        rows = stree.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row')

        verified_pairs: List[CanonicalExample] = []
        unannotated_sa: List[CanonicalExample] = []

        for idx, r in enumerate(rows[1:]):
            cells = r.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')
            row_vals = {}
            for c in cells:
                r_idx = c.get('r')
                col_letter = ''.join([ch for ch in r_idx if ch.isalpha()])
                t = c.get('t')
                v = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                v_text = v.text if v is not None else ''
                if t == 's' and v_text.isdigit():
                    val = strings[int(v_text)]
                else:
                    val = v_text
                row_vals[col_letter] = val or ''

            sentence_id = (row_vals.get('A') or f"CV_ROW_{idx+2}").strip()
            sa_text = normalize_sesotho_text(row_vals.get('B') or '')
            sim_flag = (row_vals.get('C') or '').strip()
            ls_text = normalize_sesotho_text(row_vals.get('D') or '')

            if not sa_text:
                continue

            if ls_text:
                ex = CanonicalExample(
                    example_id=f"CV_VERIFIED_{sentence_id[:12]}",
                    source_text=sa_text,
                    target_text=ls_text,
                    source_type="human_reference_single_annotator_legacy",
                    source_dataset="DS03_CV_VERIFY",
                    document_id=f"DOC_CV_{sentence_id[:8]}",
                    is_synthetic=False,
                    notes=(
                        f"LEGACY_SIMILARITY_RAW={sim_flag};"
                        "EXACT_COPY_DERIVED_FROM_TEXT;"
                        "EXPOSED_TO_RULE_DEVELOPMENT=true;"
                        "INDEPENDENT_REVIEW=pending"
                    )
                )
                verified_pairs.append(ex)
            else:
                ex = CanonicalExample(
                    example_id=f"CV_UNANNOTATED_{sentence_id[:12]}",
                    source_text=sa_text,
                    target_text="",
                    source_type="monolingual_sa",
                    source_dataset="DS03_CV_VERIFY",
                    document_id=f"DOC_CV_{sentence_id[:8]}",
                    is_synthetic=False,
                    notes="Awaiting manual annotation"
                )
                unannotated_sa.append(ex)

    return verified_pairs, unannotated_sa


def generate_synthetic_training_pairs(
    sa_sentences: List[str],
    source_dataset_id: str,
    max_pairs: Optional[int] = None
) -> List[CanonicalExample]:
    """
    Generates exploratory synthetic pairs from the development rule engine.

    These outputs are machine-generated and may be used only with explicit
    synthetic provenance. They are never human references.
    """
    engine = SesothoRuleEngine()
    synthetic_examples: List[CanonicalExample] = []

    for i, raw_sent in enumerate(sa_sentences):
        sa_clean = normalize_sesotho_text(raw_sent)
        if len(sa_clean) < 10:
            continue

        ls_target, applied_rules = engine.convert(sa_clean)
        # Keep if rules made changes and text is reasonable length
        if applied_rules and sa_clean != ls_target:
            hash_id = hashlib.sha256(sa_clean.encode('utf-8')).hexdigest()[:12]
            ex = CanonicalExample(
                example_id=f"SYNTH_{source_dataset_id}_{hash_id}",
                source_text=sa_clean,
                target_text=ls_target,
                source_type="synthetic_rule",
                source_dataset=source_dataset_id,
                document_id=f"DOC_SYNTH_{source_dataset_id}_{i // 10}",
                is_synthetic=True,
                notes=f"Rules: {','.join(applied_rules)}"
            )
            synthetic_examples.append(ex)

            if max_pairs and len(synthetic_examples) >= max_pairs:
                break

    return synthetic_examples


def split_dataset_leakage_free(
    genuine_examples: List[CanonicalExample],
    synthetic_examples: Optional[List[CanonicalExample]] = None,
    val_ratio: float = 0.2,
    test_ratio: float = 0.2,
    seed: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict]:
    """
    Partitions data into train, val, and test splits with strict guarantees:
    1. 0% synthetic data in validation or test splits (synthetic data only in train).
    2. Document-level grouping: all sentences from the same document_id stay in one split.
    3. Deterministic hashing for complete reproducibility.
    """
    import random
    rng = random.Random(seed)

    # Group genuine examples by document_id
    doc_to_examples: Dict[str, List[CanonicalExample]] = {}
    for ex in genuine_examples:
        doc_to_examples.setdefault(ex.document_id, []).append(ex)

    doc_ids = sorted(list(doc_to_examples.keys()))
    rng.shuffle(doc_ids)

    n_docs = len(doc_ids)
    n_test_docs = max(1, int(n_docs * test_ratio)) if n_docs >= 3 else 1
    n_val_docs = max(1, int(n_docs * val_ratio)) if n_docs >= 3 else 1

    test_docs = set(doc_ids[:n_test_docs])
    val_docs = set(doc_ids[n_test_docs:n_test_docs + n_val_docs])
    train_docs = set(doc_ids[n_test_docs + n_val_docs:])

    # If dataset is small, ensure train has at least something
    if not train_docs and len(doc_ids) >= 3:
        train_docs.add(doc_ids[-1])
        if doc_ids[-1] in val_docs:
            val_docs.remove(doc_ids[-1])

    train_examples: List[CanonicalExample] = []
    val_examples: List[CanonicalExample] = []
    test_examples: List[CanonicalExample] = []

    for doc_id, ex_list in doc_to_examples.items():
        if doc_id in test_docs:
            test_examples.extend(ex_list)
        elif doc_id in val_docs:
            val_examples.extend(ex_list)
        else:
            train_examples.extend(ex_list)

    # Add synthetic examples strictly to train
    if synthetic_examples:
        train_examples.extend(synthetic_examples)

    df_train = pd.DataFrame([e.to_dict() for e in train_examples])
    df_val = pd.DataFrame([e.to_dict() for e in val_examples])
    df_test = pd.DataFrame([e.to_dict() for e in test_examples])

    audit = {
        "seed": seed,
        "total_genuine_examples": len(genuine_examples),
        "total_synthetic_examples": len(synthetic_examples) if synthetic_examples else 0,
        "train_rows": len(df_train),
        "train_synthetic_rows": int(df_train["is_synthetic"].sum()) if not df_train.empty else 0,
        "val_rows": len(df_val),
        "val_synthetic_rows": int(df_val["is_synthetic"].sum()) if not df_val.empty else 0,
        "test_rows": len(df_test),
        "test_synthetic_rows": int(df_test["is_synthetic"].sum()) if not df_test.empty else 0,
        "train_doc_count": len(train_docs),
        "val_doc_count": len(val_docs),
        "test_doc_count": len(test_docs),
        "leakage_check_val_synth_zero": bool(df_val["is_synthetic"].sum() == 0) if not df_val.empty else True,
        "leakage_check_test_synth_zero": bool(df_test["is_synthetic"].sum() == 0) if not df_test.empty else True,
    }

    return df_train, df_val, df_test, audit


def load_canonical_data(file_path: str) -> pd.DataFrame:
    """Loads a processed canonical CSV file."""
    return pd.read_csv(file_path)
