"""
Unit tests for evaluation metrics (src/sesofix/metrics.py).
"""

import unittest
from src.sesofix.metrics import (
    character_edit_distance,
    word_error_rate,
    compute_all_metrics
)


class TestMetrics(unittest.TestCase):

    def test_character_edit_distance(self):
        self.assertEqual(character_edit_distance("abc", "abc"), 0)
        self.assertEqual(character_edit_distance("abc", "abd"), 1)
        self.assertEqual(character_edit_distance("abc", ""), 3)
        self.assertEqual(character_edit_distance("", "abcd"), 4)
        # SA: "dijo" vs LS: "lijo" -> 1 edit (d -> l)
        self.assertEqual(character_edit_distance("dijo", "lijo"), 1)
        # SA: "Ke a" vs LS: "Kea" -> 1 edit (delete space)
        self.assertEqual(character_edit_distance("Ke a", "Kea"), 1)

    def test_word_error_rate(self):
        self.assertEqual(word_error_rate("Ke rata ho bala", "Ke rata ho bala"), 0.0)
        self.assertEqual(word_error_rate("Ke rata ho bala", "Ke rata ho ja"), 0.25)
        self.assertEqual(word_error_rate("Ke", ""), 1.0)

    def test_compute_all_metrics(self):
        preds = ["Lijo li monate.", "Kea bala.", "Ngoana oa bapala."]
        refs = ["Lijo li monate.", "Kea bala.", "Ngoana oa bapala."]

        metrics = compute_all_metrics(preds, refs)
        self.assertEqual(metrics["count"], 3)
        self.assertEqual(metrics["exact_match_pct"], 100.0)
        self.assertEqual(metrics["avg_ced"], 0.0)
        self.assertEqual(metrics["corpus_cer_pct"], 0.0)
        self.assertEqual(metrics["corpus_wer_pct"], 0.0)
        self.assertEqual(metrics["sacrebleu"], 100.0)
        self.assertEqual(metrics["chrfpp"], 100.0)
        self.assertIn("version", metrics["sacrebleu_signature"])

    def test_changed_and_no_change_metrics(self):
        sources = ["Dijo di monate.", "Ke rata ho bala."]
        refs = ["Lijo li monate.", "Ke rata ho bala."]
        preds = ["Dijo di monate.", "Ke rata ho ja."]
        metrics = compute_all_metrics(preds, refs, sources=sources)
        self.assertEqual(metrics["changed_count"], 1)
        self.assertEqual(metrics["changed_exact_match_pct"], 0.0)
        self.assertEqual(metrics["missed_change_rate_pct"], 100.0)
        self.assertEqual(metrics["no_change_count"], 1)
        self.assertEqual(metrics["no_change_preservation_pct"], 0.0)
        self.assertEqual(metrics["unnecessary_change_rate_pct"], 100.0)


if __name__ == "__main__":
    unittest.main()
