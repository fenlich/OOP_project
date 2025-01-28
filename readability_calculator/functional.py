from typing import List, Callable
import nltk
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
import re
from math import sqrt
from .types import TokenizedSentences, SpacyTokenizedSentences

__all__ = ['get_num_words', 'get_num_sents', 'get_asl_w', 'get_n_letters', 'get_slc', 'get_n_syll', 'get_n_psyl', 'get_dep_distance', 'get_n_clauses', 'calc_flesh_kincaid', 'calc_coleman_liau_index', 'calc_SMOG_index', 'calc_ARI_index', 'calc_syntax_compl']


def get_num_words(ts: TokenizedSentences, min_syll: int = 0) -> int:
    """
    Получить количество слов в тексте
    """
    counter = 0
    for sents in ts:
        if min_syll == 0:
            counter += len(sents)
        else:
            counter += len(list(filter(lambda x: get_n_syll_in_word(x) >= min_syll, sents)))
    return counter

def get_num_sents(ts: TokenizedSentences) -> int:
    """
    Получить количество предложений в тексте
    """
    return len(ts)

def get_asl_w(ts: TokenizedSentences) -> float:
    """
    Средняя длина предложения в словах (англ. average sentence length (ASL))
    """
    num_words = get_num_words(ts)
    num_sents = get_num_sents(ts)
    try:
        avg = num_words / num_sents
    except ZeroDivisionError:
        return 0
    return avg

def  get_n_letters(ts: TokenizedSentences) -> int:
    """
    Количество букв в предложении
    """
    chars = 0
    for sent in ts:
        for word in sent:
            for ch in word:
                chars += 1
    return chars 

def get_n_ch_s(ts: TokenizedSentences) -> int:
    chars = 0
    for word in ts:
        chars += len(word)
    return chars 

def get_slc(ts: TokenizedSentences) -> float:
    """
    Средняя длина предложения в символах (анг. sentence length in characters (SLC))
    """
    chars = []
    num_sents = get_num_sents(ts)
    try:
        for sentence in ts:
            chars.append(get_n_ch_s(sentence))
            slc = sum(chars)/num_sents
    except ZeroDivisionError:
        return 0
    return slc

def get_n_syll_in_word(word: str) -> int:
    """
    Определить количество слогов в слове
    """
    vowels = 'ауоыиэяюёе'
    syl = 0
    for ch in word:
        if ch in vowels:
            syl += 1
    return syl

def get_n_syll(ts: TokenizedSentences) -> int:
    """
    Получить количество слогов в тексте
    """
    counter = 0
    for sent in ts:
        for word in sent:
            counter += get_n_syll_in_word(word)
    return counter

def get_n_psyl(ts: TokenizedSentences) -> int:
    """
    Получить слова, в которых больше 3-х слогов
    """
    return get_num_words(ts, 3)

def get_dep_distance(ts: SpacyTokenizedSentences) -> float:
    """
    Получить среднее dependency distance по формуле Liu, 2008
    """
    dd = sum([token._.dependency_distance["dependency_distance"] for token in ts])
    return dd * (1 / (len(ts) - len(list(ts.sents))))

def get_n_clauses(ts: SpacyTokenizedSentences) -> int:
    """
    Количество клауз
    """
    cnt = 0
    for token in ts:
        if 'nsubj' in token.dep_ or 'nsubj:pass' in token.dep_ or 'csubj' in token.dep_ or 'csubj:pass' in token.dep_:
            cnt += 1
    return cnt

def calc_flesh_kincaid(ts: TokenizedSentences) -> float:
    """
    Метрика Flesh Kincaid для русского языка
    """
    n_syll, n_words, asl = get_n_syll(ts), get_num_words(ts), get_asl_w(ts)
    try:
        res = 206.835 - 1.3 * (float(asl)) - 60.1 * (float(n_syll) / n_words)
    except ZeroDivisionError:
        return 0
    return abs(res)

def calc_coleman_liau_index(ts: TokenizedSentences) -> float:
    """
    Метрика Coleman Liau для русского языка
    """
    n_letters, n_words, n_sent = get_n_letters(ts), get_num_words(ts), get_num_sents(ts)
    try:
        res = 0.055 * (n_letters * (100.0 / n_words)) - 0.35 * (n_sent * (100.0 / n_words)) - 20.33
    except ZeroDivisionError:
        return 0
    return res

def calc_SMOG_index(ts: TokenizedSentences) -> float:
    """
    Метрика SMOG для русского языка
    """
    n_psyl, n_sent = get_n_psyl(ts), get_num_sents(ts)
    try:
        res = 1.1 * sqrt((float(64.6) / n_sent) * n_psyl) + 0.05
    except ZeroDivisionError:
        return 0
    return res

def calc_ARI_index(ts: TokenizedSentences) -> float:
    """ 
    Метрика Automated Readability Index (ARI) для русского языка
    """
    n_letters, n_words, n_sent = get_n_letters(ts), get_num_words(ts), get_num_sents(ts)
    try:
        res = 6.26 * (float(n_letters) / n_words) + 0.2805 * (float(n_words) / n_sent) - 31.04
    except ZeroDivisionError:
        return 0
    return res

def calc_syntax_compl(ts: TokenizedSentences, spacy_ts: SpacyTokenizedSentences) -> float:
    """
    Метрика синтаксической сложности текста
    """
    slc, dep_distance, n_clauses = get_slc(ts), get_dep_distance(spacy_ts), get_n_clauses(spacy_ts)
    res = -1.61 + 0.014 * slc + 0.146 * dep_distance + 0.057 * n_clauses
    return abs(res)  