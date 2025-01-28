from typing import List, Callable
import nltk
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
import re
from abc import ABC
import spacy_udpipe
import textdescriptives
from readability_calculator.functional import *
from .types import TokenizedSentences, SpacyTokenizedSentences


__all__ = ["Tokenizer", "NumWords", "NumSents", "ASLw", "NumLetters", "SLC", "NSyll", "NPsyll", "DependencyDist", "NClause","FleshKincaid", "ColemanLiau", "SMOG", "ARI", "Syntax"]

class _TokenizerSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Tokenizer(metaclass=_TokenizerSingleton):
    def __init__(self):
        self.setup()
        self._spacy_pipe = spacy_udpipe.load('ru')
        self._spacy_pipe.add_pipe("textdescriptives/dependency_distance")

    def setup(self,):
        nltk.download('punkt_tab')
        spacy_udpipe.download('ru')
    
    def encode(self, text: str) -> TokenizedSentences:
        sentences = sent_tokenize(text, language='russian')
        tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
        tokenized_sentences = [[token.lower() for token in sentence if not re.match(r'\W+', token)] for sentence in tokenized_sentences]
        return tokenized_sentences
    
    def encode_spacy(self, text: str) -> SpacyTokenizedSentences:
        return self._spacy_pipe(text)

def convert_to_tokens(func):
    def __inner(self, txt: str, *args, **kwargs):
        tokenizer = Tokenizer()
        if self._call_type == TokenizedSentences:
            x = tokenizer.encode(txt)
        else:
            x = tokenizer.encode_spacy(txt)
        return func(self, x, *args, **kwargs)
    return __inner

class BaseMetric(ABC):
    _call_type: TokenizedSentences | SpacyTokenizedSentences
    _call_function: Callable

    @convert_to_tokens
    def compute(self, txt: str):
        return self(txt)

    def __call__(self, ts):
        return self._call_function(ts)
    
class NumWords(BaseMetric):
    _call_type = TokenizedSentences
    _call_function = staticmethod(get_num_words)

class NumSents(BaseMetric):
    _call_type = TokenizedSentences
    _call_function = staticmethod(get_num_sents)

class ASLw(BaseMetric):
    _call_type = TokenizedSentences
    _call_function = staticmethod(get_asl_w)

class NumLetters(BaseMetric):
    _call_type = TokenizedSentences
    _call_function = staticmethod(get_n_letters)        

class SLC(BaseMetric):
    _call_type = TokenizedSentences
    _call_function = staticmethod(get_slc)

class NSyll(BaseMetric):
    _call_type = TokenizedSentences
    _call_function = staticmethod(get_n_syll)

class NPsyll(BaseMetric):
    _call_type = TokenizedSentences
    _call_function = staticmethod(get_n_psyl)

class DependencyDist(BaseMetric):
    _call_type = SpacyTokenizedSentences
    _call_function = staticmethod(get_dep_distance)

class NClause(BaseMetric):
    _call_type = SpacyTokenizedSentences
    _call_function = staticmethod(get_n_clauses)

class FleshKincaid(BaseMetric):
    _call_type = TokenizedSentences
    _call_function = staticmethod(calc_flesh_kincaid)

class ColemanLiau(BaseMetric):
    _call_type = TokenizedSentences
    _call_function = staticmethod(calc_coleman_liau_index)

class SMOG(BaseMetric):
    _call_type = TokenizedSentences
    _call_function = staticmethod(calc_SMOG_index)

class ARI(BaseMetric):
    _call_type = TokenizedSentences
    _call_function = staticmethod(calc_ARI_index)

class Syntax(BaseMetric):
    _call_function = staticmethod(calc_syntax_compl)

    def compute(self, txt: str):
        tokenizer = Tokenizer()
        ts = tokenizer.encode(txt)
        spacy_ts = tokenizer.encode_spacy(txt)
        return self(ts, spacy_ts)

    def __call__(self, ts, spacy_ts):
        return self._call_function(ts, spacy_ts)  
     