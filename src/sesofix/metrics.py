"""Transparent metrics for Sesotho cross-standard adaptation.

Corpus BLEU and chrF++ are computed with SacreBLEU and include metric
signatures. Corpus CER/WER aggregate edit counts before division. Optional source
strings enable changed/no-change safety metrics.
"""

from typing import Dict, List, Optional, Union

from sacrebleu.metrics import BLEU, CHRF


MetricValue = Union[float, int, str, None]


def _sequence_edit_distance(source: List[str], target: List[str]) -> int:
    if source == target:
        return 0
    if not source:
        return len(target)
    if not target:
        return len(source)

    previous = list(range(len(target) + 1))
    for source_index, source_item in enumerate(source, start=1):
        current = [source_index]
        for target_index, target_item in enumerate(target, start=1):
            substitution = previous[target_index - 1] + (source_item != target_item)
            current.append(
                min(
                    previous[target_index] + 1,
                    current[target_index - 1] + 1,
                    substitution,
                )
            )
        previous = current
    return previous[-1]


def character_edit_distance(source: str, target: str) -> int:
    """Levenshtein distance between two character sequences."""
    return _sequence_edit_distance(list(source), list(target))


def word_edit_distance(reference: str, hypothesis: str) -> int:
    """Levenshtein edit count between whitespace-tokenized word sequences."""
    return _sequence_edit_distance(reference.strip().split(), hypothesis.strip().split())


def word_error_rate(reference: str, hypothesis: str) -> float:
    """Sentence-level WER helper; paper results use aggregated corpus WER."""
    reference_words = reference.strip().split()
    edits = word_edit_distance(reference, hypothesis)
    if not reference_words:
        return 0.0 if edits == 0 else 1.0
    return edits / len(reference_words)


def _rate(numerator: int, denominator: int) -> Optional[float]:
    if denominator == 0:
        return None
    return round(100.0 * numerator / denominator, 2)


def compute_all_metrics(
    predictions: List[str],
    references: List[str],
    sources: Optional[List[str]] = None,
) -> Dict[str, MetricValue]:
    """Compute corpus and safety metrics on aligned strings.

    Inputs should already use the desired raw or documented normalized view. The
    function strips only leading/trailing whitespace. When ``sources`` is
    provided, it also reports changed/no-change strata.
    """
    if len(predictions) != len(references):
        raise ValueError(
            f"Predictions ({len(predictions)}) and references ({len(references)}) count mismatch"
        )
    if sources is not None and len(sources) != len(references):
        raise ValueError(
            f"Sources ({len(sources)}) and references ({len(references)}) count mismatch"
        )

    if not predictions:
        return {
            "count": 0,
            "sacrebleu": 0.0,
            "sacrebleu_signature": "",
            "chrfpp": 0.0,
            "chrfpp_signature": "",
            "avg_ced": 0.0,
            "corpus_cer_pct": 0.0,
            "corpus_wer_pct": 0.0,
            "exact_match_pct": 0.0,
            "changed_count": 0 if sources is not None else None,
            "changed_exact_match_pct": None,
            "no_change_count": 0 if sources is not None else None,
            "no_change_preservation_pct": None,
            "unnecessary_change_rate_pct": None,
            "missed_change_rate_pct": None,
        }

    preds = [str(value).strip() for value in predictions]
    refs = [str(value).strip() for value in references]
    srcs = [str(value).strip() for value in sources] if sources is not None else None

    exact_count = sum(prediction == reference for prediction, reference in zip(preds, refs))
    character_edits = [
        character_edit_distance(prediction, reference)
        for prediction, reference in zip(preds, refs)
    ]
    word_edits = [
        word_edit_distance(reference, prediction)
        for prediction, reference in zip(preds, refs)
    ]

    bleu = BLEU()
    bleu_score = bleu.corpus_score(preds, [refs]).score
    chrfpp = CHRF(word_order=2)
    chrfpp_score = chrfpp.corpus_score(preds, [refs]).score

    result: Dict[str, MetricValue] = {
        "count": len(preds),
        "sacrebleu": round(bleu_score, 2),
        "sacrebleu_signature": str(bleu.get_signature()),
        "chrfpp": round(chrfpp_score, 2),
        "chrfpp_signature": str(chrfpp.get_signature()),
        "avg_ced": round(sum(character_edits) / len(character_edits), 3),
        "corpus_cer_pct": round(
            100.0 * sum(character_edits) / max(1, sum(len(reference) for reference in refs)),
            2,
        ),
        "corpus_wer_pct": round(
            100.0
            * sum(word_edits)
            / max(1, sum(len(reference.split()) for reference in refs)),
            2,
        ),
        "exact_match_pct": round(100.0 * exact_count / len(preds), 2),
        "changed_count": None,
        "changed_exact_match_pct": None,
        "no_change_count": None,
        "no_change_preservation_pct": None,
        "unnecessary_change_rate_pct": None,
        "missed_change_rate_pct": None,
    }

    if srcs is not None:
        changed_indices = [index for index, pair in enumerate(zip(srcs, refs)) if pair[0] != pair[1]]
        unchanged_indices = [index for index, pair in enumerate(zip(srcs, refs)) if pair[0] == pair[1]]
        changed_exact = sum(preds[index] == refs[index] for index in changed_indices)
        unchanged_preserved = sum(preds[index] == srcs[index] for index in unchanged_indices)
        missed_changes = sum(preds[index] == srcs[index] for index in changed_indices)

        result.update(
            {
                "changed_count": len(changed_indices),
                "changed_exact_match_pct": _rate(changed_exact, len(changed_indices)),
                "no_change_count": len(unchanged_indices),
                "no_change_preservation_pct": _rate(
                    unchanged_preserved, len(unchanged_indices)
                ),
                "unnecessary_change_rate_pct": _rate(
                    len(unchanged_indices) - unchanged_preserved,
                    len(unchanged_indices),
                ),
                "missed_change_rate_pct": _rate(missed_changes, len(changed_indices)),
            }
        )
    return result
