#!/usr/bin/env python3
"""Read-only quality profile for the extracted Common Voice Sesotho refresh."""

from __future__ import annotations

import csv
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.sesofix.common_voice_refresh import load_legacy_workbook, match_normalize


CV_DIR = (
    PROJECT_ROOT
    / "data/incoming/common_voice/cv-corpus-26.0-2026-06-12/st"
)
LEGACY_PATH = (
    PROJECT_ROOT
    / "data/raw/common_voice_verification/Southern_Sesotho_Sentence_Verification.xlsx"
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def quantiles(values: Sequence[int]) -> Dict[str, float]:
    ordered = sorted(values)
    if not ordered:
        return {}

    def at(fraction: float) -> float:
        index = fraction * (len(ordered) - 1)
        lower = int(index)
        upper = min(lower + 1, len(ordered) - 1)
        weight = index - lower
        return round(ordered[lower] * (1 - weight) + ordered[upper] * weight, 2)

    return {
        "min": ordered[0],
        "p01": at(0.01),
        "p05": at(0.05),
        "median": round(statistics.median(ordered), 2),
        "p95": at(0.95),
        "p99": at(0.99),
        "max": ordered[-1],
    }


def duplicate_profile(rows: Sequence[Mapping[str, str]], field: str) -> Dict[str, int]:
    counts = Counter(row.get(field, "") for row in rows if row.get(field, ""))
    duplicate_groups = [count for count in counts.values() if count > 1]
    return {
        "distinct_nonempty": len(counts),
        "duplicate_groups": len(duplicate_groups),
        "rows_in_duplicate_groups": sum(duplicate_groups),
        "excess_duplicate_rows": sum(count - 1 for count in duplicate_groups),
    }


def normalized_duplicate_profile(rows: Sequence[Mapping[str, str]]) -> Dict[str, int]:
    counts = Counter(
        match_normalize(row.get("sentence", ""))
        for row in rows
        if row.get("sentence", "")
    )
    duplicate_groups = [count for count in counts.values() if count > 1]
    return {
        "distinct_nonempty": len(counts),
        "duplicate_groups": len(duplicate_groups),
        "rows_in_duplicate_groups": sum(duplicate_groups),
        "excess_duplicate_rows": sum(count - 1 for count in duplicate_groups),
    }


def overlap(left: Sequence[Mapping[str, str]], right: Sequence[Mapping[str, str]], field: str) -> int:
    left_values = {row.get(field, "") for row in left if row.get(field, "")}
    right_values = {row.get(field, "") for row in right if row.get(field, "")}
    return len(left_values & right_values)


def profile() -> Dict[str, object]:
    tsv_paths = sorted(CV_DIR.glob("*.tsv"))
    tables = {path.name: read_tsv(path) for path in tsv_paths}
    validated_sentences = tables["validated_sentences.tsv"]
    unvalidated_sentences = tables["unvalidated_sentences.tsv"]
    legacy = load_legacy_workbook(LEGACY_PATH)

    readme = (CV_DIR / "README.md").read_text(encoding="utf-8")
    release_match = re.search(r"cv-corpus-[0-9.]+-[0-9-]+", readme)
    release = release_match.group(0) if release_match else "unknown"

    legacy_by_id = {str(row["legacy_sentence_id"]): row for row in legacy}
    legacy_raw = {str(row["source_text_raw"]) for row in legacy}
    legacy_norm = {str(row["source_text_nfc_ws"]) for row in legacy}
    validated_by_id = {row["sentence_id"]: row for row in validated_sentences}
    legacy_id_exact = sum(key in validated_by_id for key in legacy_by_id)
    legacy_raw_exact = sum(str(row["source_text_raw"]) in {v["sentence"] for v in validated_sentences} for row in legacy)
    validated_norm = {match_normalize(row["sentence"]) for row in validated_sentences}
    legacy_norm_exact = sum(str(row["source_text_nfc_ws"]) in validated_norm for row in legacy)
    source_changed_on_id_match = sum(
        str(row["source_text_raw"]) != validated_by_id[str(row["legacy_sentence_id"])]["sentence"]
        for row in legacy
        if str(row["legacy_sentence_id"]) in validated_by_id
    )

    reference_rows = [row for row in legacy if row["has_human_reference"]]
    reference_id_exact = sum(str(row["legacy_sentence_id"]) in validated_by_id for row in reference_rows)
    reference_source_changed = sum(
        str(row["source_text_raw"])
        != validated_by_id[str(row["legacy_sentence_id"])]["sentence"]
        for row in reference_rows
        if str(row["legacy_sentence_id"]) in validated_by_id
    )

    new_validated = [
        row for row in validated_sentences if row["sentence_id"] not in legacy_by_id
    ]
    pending_legacy_id_overlap = sum(
        row["sentence_id"] in legacy_by_id for row in unvalidated_sentences
    )
    pending_legacy_raw_overlap = sum(
        row["sentence"] in legacy_raw for row in unvalidated_sentences
    )
    pending_legacy_norm_overlap = sum(
        match_normalize(row["sentence"]) in legacy_norm for row in unvalidated_sentences
    )

    source_counts = Counter(row.get("source", "") or "<blank>" for row in unvalidated_sentences)
    status_counts = Counter(row.get("status", "") or "<blank>" for row in unvalidated_sentences)
    vote_pairs = Counter(
        (int(row.get("up_votes") or 0), int(row.get("down_votes") or 0))
        for row in unvalidated_sentences
    )
    token_lengths = [len(row["sentence"].split()) for row in unvalidated_sentences]
    character_lengths = [len(row["sentence"]) for row in unvalidated_sentences]

    surface_flags = Counter()
    for row in unvalidated_sentences:
        sentence = row["sentence"]
        tokens = sentence.split()
        if len(tokens) < 3:
            surface_flags["under_3_tokens"] += 1
        if len(tokens) > 40:
            surface_flags["over_40_tokens"] += 1
        if re.search(r"https?://|www\.", sentence, flags=re.I):
            surface_flags["contains_url"] += 1
        if re.search(r"<[^>]+>", sentence):
            surface_flags["contains_markup"] += 1
        if any(ord(char) < 32 and char not in "\t\n\r" for char in sentence):
            surface_flags["contains_control_character"] += 1
        if any(char.isdigit() for char in sentence):
            surface_flags["contains_digit"] += 1
        if not re.search(r"[A-Za-z]", sentence):
            surface_flags["no_basic_latin_letter"] += 1

    clip_tables = ["validated.tsv", "invalidated.tsv", "other.tsv", "train.tsv", "dev.tsv", "test.tsv"]
    clip_rows = [row for name in clip_tables for row in tables[name]]
    unique_clip_paths = {row["path"] for row in clip_rows if row.get("path")}
    audio_files = {path.name for path in (CV_DIR / "clips").glob("*.mp3")}
    duration_rows = tables["clip_durations.tsv"]
    duration_files = {row["clip"] for row in duration_rows}
    unique_all_clip_records = {
        (row.get("path", ""), row.get("sentence_id", ""), row.get("client_id", ""))
        for row in clip_rows
        if row.get("path", "")
    }

    schema = {}
    for path in tsv_paths:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            schema[path.name] = next(reader, [])

    return {
        "release": release,
        "directory": str(CV_DIR),
        "table_row_counts": {name: len(rows) for name, rows in tables.items()},
        "schemas": schema,
        "validated_sentence_quality": {
            "row_count": len(validated_sentences),
            "id_profile": duplicate_profile(validated_sentences, "sentence_id"),
            "raw_text_profile": duplicate_profile(validated_sentences, "sentence"),
            "normalized_text_profile": normalized_duplicate_profile(validated_sentences),
            "invalid_sentence_ids": sum(
                not HEX64.fullmatch(row.get("sentence_id", ""))
                for row in validated_sentences
            ),
            "blank_sentence_count": sum(not row.get("sentence", "") for row in validated_sentences),
            "variant_nonempty": sum(bool(row.get("variant", "")) for row in validated_sentences),
            "domain_nonempty": sum(bool(row.get("sentence_domain", "")) for row in validated_sentences),
            "source_counts": dict(Counter(row.get("source", "") or "<blank>" for row in validated_sentences)),
        },
        "legacy_reconciliation": {
            "legacy_rows": len(legacy),
            "legacy_reference_rows": len(reference_rows),
            "validated_exact_id_matches": legacy_id_exact,
            "validated_exact_raw_text_matches": legacy_raw_exact,
            "validated_normalized_text_matches": legacy_norm_exact,
            "source_changed_on_exact_id_match": source_changed_on_id_match,
            "reference_exact_id_matches": reference_id_exact,
            "reference_source_changed_on_exact_id_match": reference_source_changed,
            "new_validated_rows": len(new_validated),
            "new_validated_records": [
                {
                    "sentence_id": row["sentence_id"],
                    "sentence": row["sentence"],
                    "source": row.get("source", ""),
                    "is_used": row.get("is_used", ""),
                    "clips_count": row.get("clips_count", ""),
                }
                for row in new_validated
            ],
        },
        "pending_sentence_quality": {
            "row_count": len(unvalidated_sentences),
            "id_profile": duplicate_profile(unvalidated_sentences, "sentence_id"),
            "raw_text_profile": duplicate_profile(unvalidated_sentences, "sentence"),
            "normalized_text_profile": normalized_duplicate_profile(unvalidated_sentences),
            "invalid_sentence_ids": sum(
                not HEX64.fullmatch(row.get("sentence_id", ""))
                for row in unvalidated_sentences
            ),
            "blank_sentence_count": sum(not row.get("sentence", "") for row in unvalidated_sentences),
            "variant_nonempty": sum(bool(row.get("variant", "")) for row in unvalidated_sentences),
            "domain_nonempty": sum(bool(row.get("sentence_domain", "")) for row in unvalidated_sentences),
            "source_counts": dict(source_counts.most_common()),
            "status_counts": dict(status_counts),
            "vote_pair_counts": {f"up={up},down={down}": count for (up, down), count in sorted(vote_pairs.items())},
            "token_length": quantiles(token_lengths),
            "character_length": quantiles(character_lengths),
            "surface_flags": dict(surface_flags),
            "overlap_with_validated_by_id": overlap(
                unvalidated_sentences, validated_sentences, "sentence_id"
            ),
            "overlap_with_validated_by_raw_text": overlap(
                unvalidated_sentences, validated_sentences, "sentence"
            ),
            "overlap_with_legacy_by_id": pending_legacy_id_overlap,
            "overlap_with_legacy_by_raw_text": pending_legacy_raw_overlap,
            "overlap_with_legacy_by_normalized_text": pending_legacy_norm_overlap,
        },
        "clip_integrity": {
            "audio_file_count": len(audio_files),
            "unique_clip_paths_in_clip_tables": len(unique_clip_paths),
            "unique_clip_records_across_overlapping_tables": len(unique_all_clip_records),
            "duration_row_count": len(duration_rows),
            "missing_audio_for_referenced_paths": sorted(unique_clip_paths - audio_files),
            "orphan_audio_files": sorted(audio_files - unique_clip_paths),
            "missing_duration_for_audio": sorted(audio_files - duration_files),
            "duration_without_audio": sorted(duration_files - audio_files),
            "validated_equals_train": tables["validated.tsv"] == tables["train.tsv"],
        },
    }


if __name__ == "__main__":
    print(json.dumps(profile(), ensure_ascii=False, indent=2, sort_keys=True))
