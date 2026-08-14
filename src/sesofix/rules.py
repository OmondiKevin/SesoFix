"""
Development rule engine for Sesotho cross-standard adaptation (South African -> Lesotho).
The rules are explicit and traceable, but they are candidate hypotheses derived
during exploratory work. They have not yet received independent linguistic
validation and must not be described as a verified catalog.
"""

import re
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set, Callable, Union


@dataclass(frozen=True)
class Rule:
    """Represents a single linguistic orthography conversion rule."""
    rule_id: str
    category: str
    description: str
    pattern: str
    replacement: Union[str, Callable]
    priority: int  # Lower number = higher execution priority
    flags: int = 0
    example_input: str = ""
    example_output: str = ""


# Exception words that should NOT undergo generic di- -> li- or d->l transformation
PHONOLOGICAL_D_EXCEPTIONS: Set[str] = {
    "dipale", "dino", "dinoe", "ditaba", "direkoto"
}


class SesothoRuleEngine:
    """
    Deterministic rule-based converter from South African Sesotho (st_ZA)
    to Lesotho Sesotho (st_LS).
    """

    def __init__(self, custom_rules: Optional[List[Rule]] = None):
        self.rules = sorted(custom_rules or self._get_default_rules(), key=lambda r: r.priority)
        self._compiled_rules = [(r, re.compile(r.pattern, r.flags)) for r in self.rules]

    @staticmethod
    def _get_default_rules() -> List[Rule]:
        """
        Builds the current development rule catalog.

        Examples and descriptions specify intended behavior; they are not
        independent evidence that a rule is universally valid.
        """
        rules = [
            # -------------------------------------------------------------
            # Category 1: Specific Lexical & Common Stems (Priority 10-25)
            # -------------------------------------------------------------
            Rule(
                rule_id="R01_LEX_JWALE",
                category="Lexical",
                description="Converts 'jwale' (now) and 'jwalo' (thus) variants to 'joale'/'joalo'",
                pattern=r"\b([Jj])wale\b",
                replacement=lambda m: "Joale" if m.group(1).isupper() else "joale",
                priority=10,
                example_input="jwale",
                example_output="joale"
            ),
            Rule(
                rule_id="R02_LEX_JWALO",
                category="Lexical",
                description="Converts 'jwalo' to 'joalo'",
                pattern=r"\b([Jj])walo\b",
                replacement=lambda m: "Joalo" if m.group(1).isupper() else "joalo",
                priority=11,
                example_input="jwalo ka",
                example_output="joalo ka"
            ),
            Rule(
                rule_id="R03_LEX_JWALOKA",
                category="Lexical",
                description="Converts merged 'jwaloka' to 'joaloka'",
                pattern=r"\b([Jj])waloka\b",
                replacement=lambda m: "Joaloka" if m.group(1).isupper() else "joaloka",
                priority=12,
                example_input="jwaloka",
                example_output="joaloka"
            ),
            Rule(
                rule_id="R04_LEX_NGWANA",
                category="Lexical",
                description="Converts 'ngwana' (child) and derivatives to 'ngoana'",
                pattern=r"\b([Nn])gwana\b",
                replacement=lambda m: "Ngoana" if m.group(1).isupper() else "ngoana",
                priority=15,
                example_input="Ngwana o a bapala",
                example_output="Ngoana o a bapala"
            ),
            Rule(
                rule_id="R05_LEX_NGWANA_DERIV",
                category="Lexical",
                description="Converts 'ngwanana' (girl) to 'ngoanana'",
                pattern=r"\b([Nn])gwanana\b",
                replacement=lambda m: "Ngoanana" if m.group(1).isupper() else "ngoanana",
                priority=16,
                example_input="ngwanana",
                example_output="ngoanana"
            ),
            Rule(
                rule_id="R06_LEX_NGWAHA",
                category="Lexical",
                description="Converts 'ngwaha' (year) to 'ngoaha'",
                pattern=r"\b([Nn])gwaha\b",
                replacement=lambda m: "Ngoaha" if m.group(1).isupper() else "ngoaha",
                priority=17,
                example_input="ngwaha",
                example_output="ngoaha"
            ),
            Rule(
                rule_id="R07_PRON_WENA",
                category="Pronoun",
                description="Converts 2nd person absolute pronoun 'wena' (you) to 'uena'",
                pattern=r"\b([Ww])ena\b",
                replacement=lambda m: "Uena" if m.group(1).isupper() else "uena",
                priority=20,
                example_input="wena",
                example_output="uena"
            ),
            Rule(
                rule_id="R08_PRON_WONA",
                category="Pronoun",
                description="Converts absolute pronoun 'wona' (it/them) to 'oona'",
                pattern=r"\b([Ww])ona\b",
                replacement=lambda m: "Oona" if m.group(1).isupper() else "oona",
                priority=21,
                example_input="wona",
                example_output="oona"
            ),
            Rule(
                rule_id="R09_VERB_SHWA",
                category="Verb",
                description="Converts 'shwa' (die) and 'shwele' (died) to 'shoa' / 'shoele'",
                pattern=r"\b([Ss])hwele\b",
                replacement=lambda m: "Shoele" if m.group(1).isupper() else "shoele",
                priority=22,
                example_input="ke shwele",
                example_output="ke shoele"
            ),
            Rule(
                rule_id="R10_VERB_TSWA",
                category="Verb",
                description="Converts 'tswa' (come from) / 'tswele' to 'tsoa' / 'tsoele'",
                pattern=r"\b([Tt])swele\b",
                replacement=lambda m: "Tsoele" if m.group(1).isupper() else "tsoele",
                priority=23,
                example_input="tswele",
                example_output="tsoele"
            ),
            Rule(
                rule_id="R11_NOUN_LENTSWE",
                category="Noun",
                description="Converts 'lentswe' (word/voice) to 'lentsoe'",
                pattern=r"\b([Ll])entswe\b",
                replacement=lambda m: "Lentsoe" if m.group(1).isupper() else "lentsoe",
                priority=24,
                example_input="lentswe",
                example_output="lentsoe"
            ),
            Rule(
                rule_id="R12_NOUN_MANTSWE",
                category="Noun",
                description="Converts 'mantswe' (words) to 'mantsoe'",
                pattern=r"\b([Mm])antswe\b",
                replacement=lambda m: "Mantsoe" if m.group(1).isupper() else "mantsoe",
                priority=25,
                example_input="mantswe",
                example_output="mantsoe"
            ),
            Rule(
                rule_id="R13_VERB_BIDIETSA",
                category="Verb",
                description="Converts 'bidietsa' to 'bilietsa'",
                pattern=r"\b([Bb])idietsa\b",
                replacement=lambda m: "Bilietsa" if m.group(1).isupper() else "bilietsa",
                priority=26,
                example_input="bidietsa",
                example_output="bilietsa"
            ),

            # -------------------------------------------------------------
            # Category 2: Copulative & Subject Concord Merging (Priority 30-45)
            # -------------------------------------------------------------
            Rule(
                rule_id="R20_COP_KEA",
                category="Copulative/Concord",
                description="Consolidates 1st person singular concord 'Ke a' -> 'Kea'",
                pattern=r"\b([Kk])e a (?=[a-zA-Z])",
                replacement=lambda m: "Kea " if m.group(1).isupper() else "kea ",
                priority=30,
                example_input="Ke a sebetsa",
                example_output="Kea sebetsa"
            ),
            Rule(
                rule_id="R21_COP_BAA",
                category="Copulative/Concord",
                description="Consolidates 3rd person plural concord 'Ba a' -> 'Baa'",
                pattern=r"\b([Bb])a a (?=[a-zA-Z])",
                replacement=lambda m: "Baa " if m.group(1).isupper() else "baa ",
                priority=31,
                example_input="Ba a kena",
                example_output="Baa kena"
            ),
            Rule(
                rule_id="R22_COP_REA",
                category="Copulative/Concord",
                description="Consolidates 1st person plural concord 'Re a' -> 'Rea'",
                pattern=r"\b([Rr])e a (?=[a-zA-Z])",
                replacement=lambda m: "Rea " if m.group(1).isupper() else "rea ",
                priority=32,
                example_input="Re a hloka",
                example_output="Rea hloka"
            ),
            Rule(
                rule_id="R23_COP_OA",
                category="Copulative/Concord",
                description="Consolidates 3rd person singular / Class 1 concord 'O a' -> 'Oa'",
                pattern=r"\b([Oo]) a (?=[a-zA-Z])",
                replacement=lambda m: "Oa " if m.group(1).isupper() else "oa ",
                priority=33,
                example_input="O a tseba",
                example_output="Oa tseba"
            ),
            Rule(
                rule_id="R24_COP_LEA",
                category="Copulative/Concord",
                description="Consolidates 2nd person plural / Class 5 concord 'Le a' -> 'Lea'",
                pattern=r"\b([Ll])e a (?=[a-zA-Z])",
                replacement=lambda m: "Lea " if m.group(1).isupper() else "lea ",
                priority=34,
                example_input="Le a bona",
                example_output="Lea bona"
            ),
            Rule(
                rule_id="R25_COP_DIA_LIA",
                category="Copulative/Concord",
                description="Consolidates Class 8/10 concord 'Di a' -> 'Lia'",
                pattern=r"\b([Dd])i a (?=[a-zA-Z])",
                replacement=lambda m: "Lia " if m.group(1).isupper() else "lia ",
                priority=35,
                example_input="Di a ja",
                example_output="Lia ja"
            ),
            Rule(
                rule_id="R26_COP_EA",
                category="Copulative/Concord",
                description="Consolidates Class 9 concord 'E a' -> 'Ea'",
                pattern=r"\b([Ee]) a (?=[a-zA-Z])",
                replacement=lambda m: "Ea " if m.group(1).isupper() else "ea ",
                priority=36,
                example_input="E a sebetsa",
                example_output="Ea sebetsa"
            ),
            Rule(
                rule_id="R27_COP_SEA",
                category="Copulative/Concord",
                description="Consolidates Class 7 concord 'Se a' -> 'Sea'",
                pattern=r"\b([Ss])e a (?=[a-zA-Z])",
                replacement=lambda m: "Sea " if m.group(1).isupper() else "sea ",
                priority=37,
                example_input="Se a tsamaya",
                example_output="Sea tsamaya"
            ),

            # -------------------------------------------------------------
            # Category 3: Possessive & Relative Particles (Priority 50-65)
            # -------------------------------------------------------------
            Rule(
                rule_id="R30_POSS_YA_EA",
                category="Possessive",
                description="Converts standalone possessive/relative marker 'ya' to 'ea'",
                pattern=r"\b([Yy])a\b",
                replacement=lambda m: "Ea" if m.group(1).isupper() else "ea",
                priority=50,
                example_input="thuso ya hao",
                example_output="thuso ea hao"
            ),
            Rule(
                rule_id="R31_POSS_WA_OA",
                category="Possessive",
                description="Converts standalone possessive marker 'wa' to 'oa'",
                pattern=r"\b([Ww])a\b",
                replacement=lambda m: "Oa" if m.group(1).isupper() else "oa",
                priority=51,
                example_input="morwa wa ka",
                example_output="morwa oa ka"
            ),
            Rule(
                rule_id="R32_DEM_YO_EO",
                category="Demonstrative",
                description="Converts demonstrative 'yo' to 'eo'",
                pattern=r"\b([Yy])o\b",
                replacement=lambda m: "Eo" if m.group(1).isupper() else "eo",
                priority=52,
                example_input="motho yo",
                example_output="motho eo"
            ),
            Rule(
                rule_id="R33_DEM_WO_OO",
                category="Demonstrative",
                description="Converts demonstrative 'wo' to 'oo'",
                pattern=r"\b([Ww])o\b",
                replacement=lambda m: "Oo" if m.group(1).isupper() else "oo",
                priority=53,
                example_input="mosebetsi wo",
                example_output="mosebetsi oo"
            ),
            Rule(
                rule_id="R34_DEM_YE_EE",
                category="Demonstrative",
                description="Converts demonstrative 'ye' to 'ee'",
                pattern=r"\b([Yy])e\b",
                replacement=lambda m: "Ee" if m.group(1).isupper() else "ee",
                priority=54,
                example_input="nako ye",
                example_output="nako ee"
            ),

            # -------------------------------------------------------------
            # Category 4: Consonant & Digraph Shifts (Priority 70-85)
            # -------------------------------------------------------------
            Rule(
                rule_id="R40_CON_TJH_CH",
                category="Consonant",
                description="Converts digraph 'tjh' or 'tj' to 'ch' (e.g. tjhaba -> chaba)",
                pattern=r"\b([Tt])jh?([a-zA-Z]+)",
                replacement=lambda m: ("Ch" if m.group(1).isupper() else "ch") + m.group(2),
                priority=70,
                example_input="Letsatsi le a tjhaba",
                example_output="Letsatsi lea chaba"
            ),
            Rule(
                rule_id="R41_CON_KG_KH",
                category="Consonant",
                description="Converts aspirated affricate 'kg' to 'kh' (e.g. kgomo -> khomo)",
                pattern=r"([Kk])g([a-zA-Z]*)",
                replacement=lambda m: ("Kh" if m.group(1).isupper() else "kh") + m.group(2),
                priority=75,
                example_input="kgomo",
                example_output="khomo"
            ),

            # -------------------------------------------------------------
            # Category 5: Initial / Prefix 'd' -> 'l' before 'i' or 'u' (Priority 90-95)
            # -------------------------------------------------------------
            Rule(
                rule_id="R50_PHON_INITIAL_D_TO_L",
                category="Phonological Allophone",
                description="Converts word-initial 'd' before 'i' or 'u' to Lesotho 'l' (e.g. dijo -> lijo, dula -> lula)",
                pattern=r"\b([Dd])([iu][a-zA-Z]*)\b",
                replacement=lambda m: (
                    m.group(0) if m.group(0).lower() in PHONOLOGICAL_D_EXCEPTIONS
                    else ("L" if m.group(1).isupper() else "l") + m.group(2)
                ),
                priority=90,
                example_input="Dijo di monate haholo.",
                example_output="Lijo li monate haholo."
            ),
            Rule(
                rule_id="R51_PRON_DI_LI",
                category="Pronoun Concord",
                description="Converts standalone Class 8/10 concord 'di' to 'li'",
                pattern=r"\b([Dd])i\b",
                replacement=lambda m: "Li" if m.group(1).isupper() else "li",
                priority=95,
                example_input="di monate",
                example_output="li monate"
            ),
        ]
        return rules

    def convert(self, text: str) -> Tuple[str, List[str]]:
        """
        Applies all rules sequentially to input text.
        Returns:
            Tuple of (converted_text, applied_rule_ids)
        """
        if not text:
            return "", []

        result = text
        applied_rules: List[str] = []

        for rule, compiled_regex in self._compiled_rules:
            if compiled_regex.search(result):
                prev_text = result
                result = compiled_regex.sub(rule.replacement, result)
                if result != prev_text:
                    applied_rules.append(rule.rule_id)

        return result, applied_rules


# Global convenience instance
_DEFAULT_ENGINE = SesothoRuleEngine()


def apply_rules(text: str) -> str:
    """Convenience function to convert text using default rule engine."""
    output, _ = _DEFAULT_ENGINE.convert(text)
    return output
