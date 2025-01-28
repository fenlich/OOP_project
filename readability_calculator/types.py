from typing import List, Callable, TypedDict
from dataclasses import dataclass

__all__ = ["TokenizedSentences", "SpacyTokenizedSentences", "CalcOutput"]

TokenizedSentences = List[List[str]]

SpacyTokenizedSentences = List

@dataclass
class CalcOutput(TypedDict):
    num_words: int | None
    num_sentences: int | None
    avg_sent_len: float | None
    num_letters: int | None
    avg_sent_len_ch: float | None
    num_syll: int | None
    num_polysyl: int | None
    dep_distance: float | None
    num_clauses: int | None
    
@dataclass
class ComplexCalcOutput(CalcOutput):
    Flesh_Kincaid: float | None
    Coleman_Liau: float | None
    SMOG: float | None
    ARI: float | None
    Syntax_compl: float | None