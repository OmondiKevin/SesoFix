"""Deterministic sampling for the Common Voice annotation pilot.

The pilot is development-only. The natural component is sampled first from the
full pending-sentence universe; coverage items are then drawn without overlap.
"""

from __future__ import annotations

import hashlib
import random
from collections import Counter
from typing import Dict, Iterable, List, Mapping, Sequence


ALGORITHM_VERSION = "pilot_v1_natural150_coverage50"
RELEASE = "cv-corpus-26.0-2026-06-12"
DEFAULT_SEED = 42
NATURAL_COUNT = 150
COVERAGE_QUOTAS = {
    "coverage_short": 15,
    "coverage_downvoted": 15,
    "coverage_non_gov_source": 20,
}


def _stable_shuffle(
    rows: Iterable[Mapping[str, str]], seed: int
) -> List[Mapping[str, str]]:
    ordered = sorted(rows, key=lambda row: row["sentence_id"])
    random.Random(seed).shuffle(ordered)
    return ordered


def _take_new(
    rows: Iterable[Mapping[str, str]],
    count: int,
    selected_ids: set[str],
    seed: int,
) -> List[Mapping[str, str]]:
    candidates = [row for row in rows if row["sentence_id"] not in selected_ids]
    shuffled = _stable_shuffle(candidates, seed)
    if len(shuffled) < count:
        raise ValueError(f"Requested {count} rows but only {len(shuffled)} eligible rows remain")
    chosen = shuffled[:count]
    selected_ids.update(row["sentence_id"] for row in chosen)
    return chosen


def select_pilot(
    pending_rows: Sequence[Mapping[str, str]], seed: int = DEFAULT_SEED
) -> List[Dict[str, object]]:
    """Return 200 unique pilot records with reproducible strata and row orders."""
    if len(pending_rows) < NATURAL_COUNT + sum(COVERAGE_QUOTAS.values()):
        raise ValueError("Pending pool is too small for the configured pilot")

    sentence_ids = [row.get("sentence_id", "") for row in pending_rows]
    if any(not sentence_id for sentence_id in sentence_ids):
        raise ValueError("Every pending row must have a sentence_id")
    duplicate_ids = [key for key, value in Counter(sentence_ids).items() if value > 1]
    if duplicate_ids:
        raise ValueError(f"Duplicate sentence IDs found: {duplicate_ids[:5]}")
    if any(row.get("status", "") != "pending" for row in pending_rows):
        raise ValueError("Pilot selection expects only rows with status=pending")

    selected_ids: set[str] = set()
    selections: List[tuple[Mapping[str, str], str]] = []

    natural = _take_new(pending_rows, NATURAL_COUNT, selected_ids, seed)
    selections.extend((row, "natural_random") for row in natural)

    short_rows = [row for row in pending_rows if len(row.get("sentence", "").split()) < 3]
    downvoted_rows = [row for row in pending_rows if int(row.get("down_votes") or 0) > 0]
    non_gov_rows = [
        row
        for row in pending_rows
        if (row.get("source", "").strip() or "<blank>") != "*.gov.za"
    ]
    coverage_pools = {
        "coverage_short": short_rows,
        "coverage_downvoted": downvoted_rows,
        "coverage_non_gov_source": non_gov_rows,
    }

    for offset, (stratum, quota) in enumerate(COVERAGE_QUOTAS.items(), start=1):
        chosen = _take_new(
            coverage_pools[stratum], quota, selected_ids, seed + offset
        )
        selections.extend((row, stratum) for row in chosen)

    stable_records = sorted(selections, key=lambda item: item[0]["sentence_id"])
    pilot_ids = {
        row["sentence_id"]: f"PILOT-{index:04d}"
        for index, (row, _) in enumerate(stable_records, start=1)
    }

    primary_order_ids = [row["sentence_id"] for row, _ in selections]
    random.Random(seed + 101).shuffle(primary_order_ids)
    reviewer_order_ids = [row["sentence_id"] for row, _ in selections]
    random.Random(seed + 202).shuffle(reviewer_order_ids)
    primary_order = {sentence_id: index for index, sentence_id in enumerate(primary_order_ids, 1)}
    reviewer_order = {sentence_id: index for index, sentence_id in enumerate(reviewer_order_ids, 1)}

    output: List[Dict[str, object]] = []
    for row, stratum in selections:
        sentence = row.get("sentence", "")
        output.append(
            {
                "release": RELEASE,
                "pilot_id": pilot_ids[row["sentence_id"]],
                "sentence_id": row["sentence_id"],
                "source_text": sentence,
                "source_sha256": hashlib.sha256(sentence.encode("utf-8")).hexdigest(),
                "sample_role": "pilot_development_only",
                "selection_stratum": stratum,
                "source_name": row.get("source", "").strip(),
                "up_votes": int(row.get("up_votes") or 0),
                "down_votes": int(row.get("down_votes") or 0),
                "token_count": len(sentence.split()),
                "primary_order": primary_order[row["sentence_id"]],
                "reviewer_order": reviewer_order[row["sentence_id"]],
                "selection_seed": seed,
                "algorithm_version": ALGORITHM_VERSION,
            }
        )
    return sorted(output, key=lambda row: row["pilot_id"])


def validate_pilot(records: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    """Return compact invariants; raise when the frozen design is violated."""
    if len(records) != 200:
        raise ValueError(f"Expected 200 pilot rows, found {len(records)}")
    pilot_ids = [str(record["pilot_id"]) for record in records]
    expected_pilot_ids = {f"PILOT-{index:04d}" for index in range(1, 201)}
    if set(pilot_ids) != expected_pilot_ids:
        raise ValueError("Pilot IDs are not the complete PILOT-0001..PILOT-0200 set")
    ids = [str(record["sentence_id"]) for record in records]
    if len(set(ids)) != len(ids):
        raise ValueError("Pilot contains duplicate sentence IDs")
    if any(len(str(record["source_sha256"])) != 64 for record in records):
        raise ValueError("Every pilot row must have a SHA-256 source hash")
    if {str(record["sample_role"]) for record in records} != {
        "pilot_development_only"
    }:
        raise ValueError("Every pilot row must remain development-only")
    selection_seeds = {int(record["selection_seed"]) for record in records}
    if len(selection_seeds) != 1:
        raise ValueError("Pilot selection seed is inconsistent")
    if {str(record["algorithm_version"]) for record in records} != {
        ALGORITHM_VERSION
    }:
        raise ValueError("Pilot algorithm version is inconsistent")
    strata = Counter(str(record["selection_stratum"]) for record in records)
    expected = {"natural_random": NATURAL_COUNT, **COVERAGE_QUOTAS}
    if dict(strata) != expected:
        raise ValueError(f"Unexpected strata: {dict(strata)}; expected {expected}")
    if sorted(int(record["primary_order"]) for record in records) != list(range(1, 201)):
        raise ValueError("Primary workbook order is not a complete 1..200 permutation")
    if sorted(int(record["reviewer_order"]) for record in records) != list(range(1, 201)):
        raise ValueError("Reviewer workbook order is not a complete 1..200 permutation")
    primary_sequence = sorted(records, key=lambda record: int(record["primary_order"]))
    reviewer_sequence = sorted(records, key=lambda record: int(record["reviewer_order"]))
    if [record["sentence_id"] for record in primary_sequence] == [
        record["sentence_id"] for record in reviewer_sequence
    ]:
        raise ValueError("Primary and reviewer workbook orders must differ")
    return {
        "row_count": len(records),
        "unique_sentence_ids": len(set(ids)),
        "strata": expected,
        "seed": selection_seeds.pop(),
        "algorithm_version": str(records[0]["algorithm_version"]),
    }
