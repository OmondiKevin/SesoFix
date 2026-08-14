"""Tests for deterministic, contamination-aware pilot selection."""

import unittest

from src.sesofix.pilot_sampling import select_pilot, validate_pilot


def fixture_rows(count: int = 1000):
    rows = []
    for index in range(count):
        if index < 100:
            source = "Peace Corps"
        else:
            source = "*.gov.za"
        sentence = f"Sentence number {index} has enough words."
        if index < 50:
            sentence = f"Word{index}"
        rows.append(
            {
                "sentence_id": f"{index:064x}",
                "sentence": sentence,
                "source": source,
                "up_votes": "0",
                "down_votes": "1" if 50 <= index < 100 else "0",
                "status": "pending",
            }
        )
    return rows


class TestPilotSampling(unittest.TestCase):
    def test_selection_is_reproducible_and_valid(self):
        first = select_pilot(fixture_rows(), seed=42)
        second = select_pilot(list(reversed(fixture_rows())), seed=42)
        self.assertEqual(first, second)
        summary = validate_pilot(first)
        self.assertEqual(summary["row_count"], 200)
        self.assertEqual(summary["strata"]["natural_random"], 150)
        self.assertEqual(summary["strata"]["coverage_short"], 15)
        self.assertEqual(summary["strata"]["coverage_downvoted"], 15)
        self.assertEqual(summary["strata"]["coverage_non_gov_source"], 20)
        primary = sorted(first, key=lambda record: int(record["primary_order"]))
        reviewer = sorted(first, key=lambda record: int(record["reviewer_order"]))
        self.assertNotEqual(
            [record["sentence_id"] for record in primary],
            [record["sentence_id"] for record in reviewer],
        )

    def test_source_text_is_hashed_but_retained_for_workbook_build(self):
        records = select_pilot(fixture_rows(), seed=42)
        self.assertTrue(all(len(str(record["source_sha256"])) == 64 for record in records))
        self.assertTrue(all(record["source_text"] for record in records))


if __name__ == "__main__":
    unittest.main()
