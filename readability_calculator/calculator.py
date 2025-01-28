from typing import List, Dict, Tuple, NamedTuple, TypedDict, Optional, Literal
from readability_calculator.base import *
from readability_calculator.types import CalcOutput

AVAILABLE_METRICS = {
    "num_words": NumWords,
    "num_sentences": NumSents,
    "avg_sent_len": ASLw,
    "num_letters": NumLetters,
    "avg_sent_len_ch": SLC,
    "num_syll": NSyll,
    "num_polysyl": NPsyll,
    "dep_distance": DependencyDist,
    "num_clauses": NClause 
}

COMPLEX_METRICS = {
    "Flesh_Kincaid": FleshKincaid,
    "Coleman_Liau": ColemanLiau,
    "SMOG": SMOG,
    "ARI": ARI,
    "Syntax_compl": Syntax
}

class Calc:
    def __init__(self, metrics_to_calculate: Optional[List[str]] = None):
        if metrics_to_calculate is None:
            metrics_to_calculate = AVAILABLE_METRICS
        self.metrics_to_calculate = {k: v() for k,v in metrics_to_calculate.items() if k in AVAILABLE_METRICS}

    def __call__(self, text: str) -> Dict[str, float | int]:
        result_dict = {}
        for k, v in self.metrics_to_calculate.items():
            result_dict[k] = v.compute(text)
        return result_dict

    def __repr__(self):
        return f"{self.__class__.__name__} with metrics {list(self.metrics_to_calculate.keys())}"
    
class ComplexCalc(Calc):
    def __init__(self, metrics_to_calculate: Optional[List[str]] = None):
        if metrics_to_calculate is None:
            metrics_to_calculate = COMPLEX_METRICS
        self.metrics_to_calculate = {k: v() for k,v in metrics_to_calculate.items() if k in COMPLEX_METRICS}