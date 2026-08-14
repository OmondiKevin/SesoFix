"""
Unit tests for Sesotho linguistic rule engine (src/sesofix/rules.py).
"""

import unittest
from src.sesofix.rules import SesothoRuleEngine, apply_rules


class TestSesothoRuleEngine(unittest.TestCase):

    def setUp(self):
        self.engine = SesothoRuleEngine()

    def test_copulative_concord_merging(self):
        # Ke a -> Kea
        self.assertEqual(self.engine.convert("Ke a sebetsa kajeno.")[0], "Kea sebetsa kajeno.")
        self.assertEqual(self.engine.convert("ke a rata ho bala.")[0], "kea rata ho bala.")

        # Ba a -> Baa
        self.assertEqual(self.engine.convert("Ba a kena sekolong.")[0], "Baa kena sekolong.")

        # Re a -> Rea
        self.assertEqual(self.engine.convert("Re a hloka thuso.")[0], "Rea hloka thuso.")

        # O a -> Oa
        self.assertEqual(self.engine.convert("O a tseba Sesotho.")[0], "Oa tseba Sesotho.")

        # Di a -> Lia
        self.assertEqual(self.engine.convert("Diphofolo di a ja.")[0], "Liphofolo lia ja.")

    def test_possessive_and_relative_vowels(self):
        # ya -> ea
        self.assertEqual(self.engine.convert("thuso ya hao")[0], "thuso ea hao")
        self.assertEqual(self.engine.convert("Nako ya ho ja")[0], "Nako ea ho ja")

        # wa -> oa
        self.assertEqual(self.engine.convert("morwa wa ka")[0], "morwa oa ka")

        # yo -> eo
        self.assertEqual(self.engine.convert("motho yo")[0], "motho eo")

        # ye -> ee
        self.assertEqual(self.engine.convert("nako ye")[0], "nako ee")

    def test_lexical_stems_and_pronouns(self):
        # jwale -> joale
        self.assertEqual(self.engine.convert("Jwale re ka tsamaya.")[0], "Joale re ka tsamaya.")
        self.assertEqual(self.engine.convert("jwalo ka mehla")[0], "joalo ka mehla")

        # ngwana -> ngoana
        self.assertEqual(self.engine.convert("Ngwana o a bapala ka ntle.")[0], "Ngoana oa bapala ka ntle.")
        self.assertEqual(self.engine.convert("ngwaha o mocha")[0], "ngoaha o mocha")

        # wena -> uena
        self.assertEqual(self.engine.convert("Nna le wena re dula hae.")[0], "Nna le uena re lula hae.")

        # shwele -> shoele
        self.assertEqual(self.engine.convert("Ke re ke se ke shwele ke tlala.")[0], "Ke re ke se ke shoele ke tlala.")

        # bidietsa -> bilietsa
        self.assertEqual(self.engine.convert("Ditoro tsena di bidietsa ho hong.")[0], "Litoro tsena li bilietsa ho hong.")

    def test_consonant_digraphs(self):
        # kg -> kh (and preserves khudu)
        self.assertEqual(self.engine.convert("E ne e se kgudu kapa kgomo.")[0], "E ne e se khudu kapa khomo.")
        self.assertEqual(self.engine.convert("makgethe a matle")[0], "makhethe a matle")

        # tj / tjh -> ch
        self.assertEqual(self.engine.convert("Letsatsi le a tjhaba.")[0], "Letsatsi lea chaba.")

    def test_noun_class_di_to_li_and_exceptions(self):
        # Regular di- -> li-
        self.assertEqual(self.engine.convert("Dijo di monate haholo.")[0], "Lijo li monate haholo.")
        self.assertEqual(self.engine.convert("Ke rata ho bala dibuka.")[0], "Ke rata ho bala libuka.")

        # Exception preservation
        res, _ = self.engine.convert("dipale tsa bo-ntate")
        self.assertIn("dipale", res)

    def test_rule_trace_logging(self):
        converted, rule_ids = self.engine.convert("Ke a ja dijo jwale.")
        self.assertIn("R20_COP_KEA", rule_ids)
        self.assertIn("R01_LEX_JWALE", rule_ids)
        self.assertIn("R50_PHON_INITIAL_D_TO_L", rule_ids)
        self.assertEqual(converted, "Kea ja lijo joale.")


if __name__ == "__main__":
    unittest.main()
