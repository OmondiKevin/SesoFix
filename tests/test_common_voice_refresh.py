"""Engineering tests for strict, lossless Common Voice matching."""

import unittest

from src.sesofix.common_voice_refresh import (
    canonicalize_fresh_records,
    match_legacy_to_fresh,
    match_normalize,
    sha256_text,
)


class TestCommonVoiceRefresh(unittest.TestCase):
    def test_matching_normalization_is_conservative(self):
        self.assertEqual(match_normalize("  Ke\t  rata\nho bala. "), "Ke rata ho bala.")
        self.assertEqual(match_normalize("e\u0301"), "é")
        self.assertNotEqual(match_normalize("ya"), "ea")

    def test_repeated_tsv_appearances_are_retained(self):
        rows = [
            {
                "source_file": "validated.tsv",
                "source_split": "validated",
                "cv_sentence_id": "abc",
                "source_text_raw": "Ke rata ho bala.",
                "clip_path": "clips/a.mp3",
                "locale": "st",
            },
            {
                "source_file": "train.tsv",
                "source_split": "train",
                "cv_sentence_id": "abc",
                "source_text_raw": "Ke rata ho bala.",
                "clip_path": "clips/a.mp3",
                "locale": "st",
            },
        ]
        fresh = canonicalize_fresh_records(rows, "cv-test")
        self.assertEqual(len(fresh), 1)
        self.assertEqual(fresh[0]["source_files"], "train.tsv|validated.tsv")
        self.assertEqual(fresh[0]["source_splits"], "train|validated")

    def test_match_tiers_and_ambiguity_quarantine(self):
        fresh = [
            {
                "fresh_key": "new:id-1:a",
                "cv_sentence_id": "id-1",
                "source_text_raw": "Ké rata.",
                "source_text_nfc_ws": "Ké rata.",
            },
            {
                "fresh_key": "new:id-2:b",
                "cv_sentence_id": "id-2",
                "source_text_raw": "Same text",
                "source_text_nfc_ws": "Same text",
            },
            {
                "fresh_key": "new:id-3:c",
                "cv_sentence_id": "id-3",
                "source_text_raw": "Same text",
                "source_text_nfc_ws": "Same text",
            },
        ]
        legacy = [
            {
                "legacy_workbook_row": 2,
                "legacy_sentence_id": "id-1",
                "source_text_raw": "different cached text",
                "source_text_nfc_ws": "different cached text",
                "has_human_reference": True,
            },
            {
                "legacy_workbook_row": 3,
                "legacy_sentence_id": "",
                "source_text_raw": "Ke\u0301 rata.",
                "source_text_nfc_ws": match_normalize("Ke\u0301 rata."),
                "has_human_reference": True,
            },
            {
                "legacy_workbook_row": 4,
                "legacy_sentence_id": "",
                "source_text_raw": "Same text",
                "source_text_nfc_ws": "Same text",
                "has_human_reference": False,
            },
        ]
        matches = match_legacy_to_fresh(legacy, fresh)
        self.assertEqual(matches[0]["match_method"], "sentence_id_exact")
        self.assertTrue(matches[0]["source_text_changed"])
        self.assertEqual(matches[1]["match_method"], "nfc_whitespace_exact")
        self.assertEqual(matches[1]["match_status"], "matched")
        self.assertEqual(matches[2]["match_status"], "ambiguous_quarantine")
        self.assertEqual(matches[2]["candidate_count"], 2)

    def test_hash_is_stable(self):
        self.assertEqual(len(sha256_text("Sesotho")), 64)
        self.assertEqual(sha256_text("Sesotho"), sha256_text("Sesotho"))


if __name__ == "__main__":
    unittest.main()
