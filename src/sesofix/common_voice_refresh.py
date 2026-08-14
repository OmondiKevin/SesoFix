"""Lossless Common Voice inventory and legacy-annotation matching.

This module performs data preparation only. It does not train or run a model.
Automatic matching stops at Unicode-NFC/whitespace equality; fuzzy candidates
require human review and are never silently accepted.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import tarfile
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Mapping, Sequence, Tuple


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def match_normalize(text: str) -> str:
    """Conservative matching view: Unicode NFC plus whitespace collapse only."""
    nfc = unicodedata.normalize("NFC", text or "")
    return re.sub(r"\s+", " ", nfc).strip()


def _iter_tsv_streams(source: Path) -> Iterator[Tuple[str, io.TextIOBase]]:
    """Yield `(member_name, text_stream)` without extracting an archive."""
    if source.is_dir():
        for path in sorted(source.rglob("*.tsv")):
            yield str(path.relative_to(source)), path.open(
                "r", encoding="utf-8-sig", newline=""
            )
        return

    if tarfile.is_tarfile(source):
        with tarfile.open(source, "r:*") as archive:
            for member in sorted(archive.getmembers(), key=lambda item: item.name):
                if not member.isfile() or not member.name.lower().endswith(".tsv"):
                    continue
                raw = archive.extractfile(member)
                if raw is None:
                    continue
                yield member.name, io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
        return

    if zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as archive:
            for name in sorted(archive.namelist()):
                if name.endswith("/") or not name.lower().endswith(".tsv"):
                    continue
                yield name, io.TextIOWrapper(
                    archive.open(name, "r"), encoding="utf-8-sig", newline=""
                )
        return

    raise ValueError(f"Expected a directory, tar archive, or zip archive: {source}")


def load_common_voice_records(source: Path) -> Tuple[List[Dict[str, str]], List[Dict[str, object]]]:
    """Read every sentence-bearing TSV row and return file-level inventory."""
    records: List[Dict[str, str]] = []
    files: List[Dict[str, object]] = []

    for member_name, stream in _iter_tsv_streams(source):
        try:
            reader = csv.DictReader(stream, delimiter="\t")
            fieldnames = list(reader.fieldnames or [])
            row_count = 0
            sentence_count = 0
            for row in reader:
                row_count += 1
                sentence = row.get("sentence") or row.get("text") or ""
                if not sentence:
                    continue
                sentence_count += 1
                records.append(
                    {
                        "source_file": member_name,
                        "source_split": Path(member_name).stem,
                        "cv_sentence_id": row.get("sentence_id") or "",
                        "source_text_raw": sentence,
                        "clip_path": row.get("path") or "",
                        "locale": row.get("locale") or "",
                    }
                )
            files.append(
                {
                    "source_file": member_name,
                    "columns": fieldnames,
                    "row_count": row_count,
                    "sentence_row_count": sentence_count,
                }
            )
        finally:
            stream.close()

    if not files:
        raise ValueError(f"No TSV files found in {source}")
    if not records:
        raise ValueError(f"TSV files contained no `sentence` or `text` values in {source}")
    return records, files


def canonicalize_fresh_records(
    records: Iterable[Mapping[str, str]], release: str
) -> List[Dict[str, str]]:
    """Collapse repeated TSV appearances while retaining duplicate clusters."""
    grouped: Dict[Tuple[str, str], Dict[str, object]] = {}

    for row in records:
        raw = row.get("source_text_raw", "")
        if not raw:
            continue
        raw_hash = sha256_text(raw)
        sentence_id = row.get("cv_sentence_id", "")
        key = (sentence_id, raw_hash)
        if key not in grouped:
            match_view = match_normalize(raw)
            grouped[key] = {
                "cv_release": release,
                "cv_sentence_id": sentence_id,
                "source_text_raw": raw,
                "source_text_nfc_ws": match_view,
                "source_sha256_raw": raw_hash,
                "source_sha256_match": sha256_text(match_view),
                "source_files": set(),
                "source_splits": set(),
                "clip_paths": set(),
                "locales": set(),
            }
        item = grouped[key]
        for source_key, destination_key in (
            ("source_file", "source_files"),
            ("source_split", "source_splits"),
            ("clip_path", "clip_paths"),
            ("locale", "locales"),
        ):
            value = row.get(source_key, "")
            if value:
                item[destination_key].add(value)  # type: ignore[union-attr]

    output: List[Dict[str, str]] = []
    for item in grouped.values():
        raw_hash = str(item["source_sha256_raw"])
        sentence_id = str(item["cv_sentence_id"])
        canonical_id = sentence_id or f"TEXT_{raw_hash[:20]}"
        output.append(
            {
                "fresh_key": f"{release}:{canonical_id}:{raw_hash[:12]}",
                "cv_release": str(item["cv_release"]),
                "cv_sentence_id": sentence_id,
                "source_text_raw": str(item["source_text_raw"]),
                "source_text_nfc_ws": str(item["source_text_nfc_ws"]),
                "source_sha256_raw": raw_hash,
                "source_sha256_match": str(item["source_sha256_match"]),
                "duplicate_cluster_id": f"TXT_{str(item['source_sha256_match'])[:20]}",
                "source_files": "|".join(sorted(item["source_files"])),  # type: ignore[arg-type]
                "source_splits": "|".join(sorted(item["source_splits"])),  # type: ignore[arg-type]
                "clip_paths": "|".join(sorted(item["clip_paths"])),  # type: ignore[arg-type]
                "locales": "|".join(sorted(item["locales"])),  # type: ignore[arg-type]
            }
        )
    return sorted(output, key=lambda row: row["fresh_key"])


def _shared_strings(archive: zipfile.ZipFile) -> List[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    strings: List[str] = []
    for item in root.findall(f"{{{MAIN_NS}}}si"):
        strings.append("".join(node.text or "" for node in item.iter(f"{{{MAIN_NS}}}t")))
    return strings


def _cell_value(cell: ET.Element, shared: Sequence[str]) -> str:
    cell_type = cell.get("t", "")
    value = cell.find(f"{{{MAIN_NS}}}v")
    raw = value.text if value is not None and value.text is not None else ""
    if cell_type == "s" and raw.isdigit():
        return shared[int(raw)]
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.iter(f"{{{MAIN_NS}}}t"))
    return raw


def load_legacy_workbook(path: Path) -> List[Dict[str, object]]:
    """Read the known four-column workbook while preserving formula evidence."""
    with zipfile.ZipFile(path) as archive:
        shared = _shared_strings(archive)
        root = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))

    output: List[Dict[str, object]] = []
    rows = root.findall(f".//{{{MAIN_NS}}}row")
    for row in rows[1:]:
        cells: Dict[str, ET.Element] = {}
        for cell in row.findall(f"{{{MAIN_NS}}}c"):
            ref = cell.get("r", "")
            column = "".join(char for char in ref if char.isalpha())
            cells[column] = cell

        raw_source = _cell_value(cells["B"], shared) if "B" in cells else ""
        if not raw_source:
            continue
        raw_target = _cell_value(cells["D"], shared) if "D" in cells else ""
        similarity = _cell_value(cells["C"], shared) if "C" in cells else ""
        target_formula = ""
        target_formula_attributes = ""
        target_was_formula = False
        if "D" in cells:
            formula = cells["D"].find(f"{{{MAIN_NS}}}f")
            if formula is not None:
                target_was_formula = True
                target_formula = formula.text or ""
                target_formula_attributes = json.dumps(
                    dict(formula.attrib), ensure_ascii=False, sort_keys=True
                )

        source_match = match_normalize(raw_source)
        target_match = match_normalize(raw_target)
        output.append(
            {
                "legacy_workbook_row": int(row.get("r", "0")),
                "legacy_sentence_id": _cell_value(cells["A"], shared) if "A" in cells else "",
                "source_text_raw": raw_source,
                "source_text_nfc_ws": source_match,
                "source_sha256_raw": sha256_text(raw_source),
                "source_sha256_match": sha256_text(source_match),
                "legacy_similarity_raw": similarity,
                "target_text_raw": raw_target,
                "target_sha256_raw": sha256_text(raw_target) if raw_target else "",
                "target_was_formula": target_was_formula,
                "target_formula": target_formula,
                "target_formula_attributes": target_formula_attributes,
                "reference_surface_origin": (
                    "formula_copy_or_formula_result" if raw_target and target_was_formula
                    else "direct_cell" if raw_target
                    else "unannotated"
                ),
                "has_human_reference": bool(raw_target),
                "exact_copy_derived": bool(raw_target and source_match == target_match),
                "single_annotator_reference": bool(raw_target),
                "exposed_to_rule_development": bool(raw_target),
                "independent_review_status": "pending" if raw_target else "not_applicable",
            }
        )
    return output


def _unique_index(rows: Sequence[Mapping[str, str]], field: str) -> Dict[str, List[int]]:
    index: Dict[str, List[int]] = defaultdict(list)
    for position, row in enumerate(rows):
        value = row.get(field, "")
        if value:
            index[value].append(position)
    return index


def match_legacy_to_fresh(
    legacy_rows: Sequence[Mapping[str, object]], fresh_rows: Sequence[Mapping[str, str]]
) -> List[Dict[str, object]]:
    """Match with strict tiers and quarantine every ambiguous case."""
    indexes = {
        "sentence_id_exact": _unique_index(fresh_rows, "cv_sentence_id"),
        "raw_text_exact": _unique_index(fresh_rows, "source_text_raw"),
        "nfc_whitespace_exact": _unique_index(fresh_rows, "source_text_nfc_ws"),
    }
    output: List[Dict[str, object]] = []

    for legacy in legacy_rows:
        tiers = (
            ("sentence_id_exact", str(legacy.get("legacy_sentence_id", ""))),
            ("raw_text_exact", str(legacy.get("source_text_raw", ""))),
            ("nfc_whitespace_exact", str(legacy.get("source_text_nfc_ws", ""))),
        )
        method = "unmatched"
        candidates: List[int] = []
        for tier, value in tiers:
            if not value:
                continue
            tier_candidates = indexes[tier].get(value, [])
            if tier_candidates:
                method = tier
                candidates = tier_candidates
                break

        if len(candidates) == 1:
            fresh = fresh_rows[candidates[0]]
            status = "matched"
            fresh_key = fresh["fresh_key"]
            changed = legacy.get("source_text_raw", "") != fresh.get("source_text_raw", "")
        elif len(candidates) > 1:
            status = "ambiguous_quarantine"
            fresh_key = "|".join(fresh_rows[index]["fresh_key"] for index in candidates)
            changed = ""
        else:
            status = "unmatched"
            fresh_key = ""
            changed = ""

        output.append(
            {
                "legacy_workbook_row": legacy.get("legacy_workbook_row", ""),
                "legacy_sentence_id": legacy.get("legacy_sentence_id", ""),
                "has_human_reference": legacy.get("has_human_reference", False),
                "fresh_key": fresh_key,
                "match_status": status,
                "match_method": method,
                "candidate_count": len(candidates),
                "source_text_changed": changed,
            }
        )
    return output


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write an empty table: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def prepare_refresh(
    archive_path: Path, legacy_workbook: Path, release: str, output_dir: Path
) -> Dict[str, object]:
    """Create an append-only refresh package; refuse a pre-existing output path."""
    if output_dir.exists():
        raise FileExistsError(
            f"Output already exists; choose a new immutable directory: {output_dir}"
        )
    output_dir.mkdir(parents=True)

    records, file_inventory = load_common_voice_records(archive_path)
    fresh_rows = canonicalize_fresh_records(records, release)
    legacy_rows = load_legacy_workbook(legacy_workbook)
    matches = match_legacy_to_fresh(legacy_rows, fresh_rows)

    write_csv(output_dir / "fresh_sentence_inventory.csv", fresh_rows)
    write_csv(output_dir / "legacy_workbook_inventory.csv", legacy_rows)
    write_csv(output_dir / "legacy_to_fresh_matches.csv", matches)

    status_counts: Dict[str, int] = defaultdict(int)
    reference_status_counts: Dict[str, int] = defaultdict(int)
    for match in matches:
        status_counts[str(match["match_status"])] += 1
        if match["has_human_reference"]:
            reference_status_counts[str(match["match_status"])] += 1

    summary: Dict[str, object] = {
        "protocol": "lossless_common_voice_refresh_v1",
        "release": release,
        "archive_path_as_supplied": str(archive_path),
        "archive_sha256": sha256_file(archive_path) if archive_path.is_file() else None,
        "legacy_workbook_path_as_supplied": str(legacy_workbook),
        "legacy_workbook_sha256": sha256_file(legacy_workbook),
        "tsv_files": file_inventory,
        "fresh_sentence_records": len(fresh_rows),
        "fresh_duplicate_clusters": len({row["duplicate_cluster_id"] for row in fresh_rows}),
        "legacy_source_rows": len(legacy_rows),
        "legacy_human_reference_rows": sum(bool(row["has_human_reference"]) for row in legacy_rows),
        "match_status_all_legacy_rows": dict(status_counts),
        "match_status_human_reference_rows": dict(reference_status_counts),
        "automatic_fuzzy_matches": 0,
        "training_performed": False,
    }
    with (output_dir / "refresh_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return summary
