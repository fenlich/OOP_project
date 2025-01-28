import unittest
from readability_calculator import *

SIMPLE_TEXT = 'Жизнь пренеприятная штука, но сделать ее прекрасной очень нетрудно.'
COMPLEX_TEXT = 'Рибоза восстанавливается водородом или амальгамой натрия до соответствующего альдита (рибита) и окисляется по альдегидной группе до соответствующей альдоновой (рибоновой) кислоты, способной циклизоваться в условиях синтеза в рибонолактон[2]. С гидразинами образует озазоны.'

def get_ts(txt):
    return Tokenizer().encode(txt)

def get_tsu(txt):
    return Tokenizer().encode_spacy(txt)

class TestFunctional(unittest.TestCase):

    def setUp(self):
        self.ts_s = get_ts(SIMPLE_TEXT)
        self.ts_c = get_ts(COMPLEX_TEXT)
        self.tsu_s = get_tsu(SIMPLE_TEXT)
        self.tsu_c = get_tsu(COMPLEX_TEXT)
        self.num_words = get_num_words
        self.num_sents = get_num_sents
        self.asl = get_asl_w
        self.num_letters = get_n_letters
        self.slc = get_slc
        self.num_syll = get_n_syll
        self.num_psyl = get_n_psyl
        self.dep_dist = get_dep_distance
        self.num_clauses = get_n_clauses
        self.fleshkinc = calc_flesh_kincaid
        self.colemanliau = calc_coleman_liau_index
        self.smog = calc_SMOG_index
        self.ari = calc_ARI_index
        self.syntaxcompl = calc_syntax_compl


    def test_num_words(self):
        a = self.num_words(self.ts_s)
        self.assertEqual(a, 9)
        b = self.num_words(self.ts_c)
        self.assertEqual(b, 32)

    def test_num_sents(self):
        a = self.num_sents(self.ts_s)
        self.assertEqual(a, 1)
        b = self.num_sents(self.ts_c)
        self.assertEqual(b, 2)

    def test_asl(self):
        a = self.asl(self.ts_s)
        self.assertEqual(a, 9.0)
        b = self.asl(self.ts_c)
        self.assertEqual(b, 16.0)
  
    def test_num_letters(self):
        a = self.num_letters(self.ts_s)
        self.assertEqual(a, 57)
        b = self.num_letters(self.ts_c)
        self.assertEqual(b, 234)

    def test_slc(self):
        a = self.slc(self.ts_s)
        self.assertEqual(a, 57)
        b = self.slc(self.ts_c)
        self.assertEqual(b, 117.0)

    def test_num_syll(self):
        a = self.num_syll(self.ts_s)
        self.assertEqual(a, 22)
        b = self.num_syll(self.ts_c)
        self.assertEqual(b, 101)

    def test_num_psyl(self):
        a = self.num_psyl(self.ts_s)
        self.assertEqual(a, 3)
        b = self.num_psyl(self.ts_c)
        self.assertEqual(b, 22)
    
    def test_dep_dist(self):
        a = self.dep_dist(self.tsu_s)
        self.assertEqual(a, 3.7)
        b = self.dep_dist(self.tsu_c)
        self.assertEqual(b, 3.1025641025641026)

    def test_num_clauses(self):
        a = self.num_clauses(self.tsu_s)
        self.assertEqual(a, 2)
        b = self.num_clauses(self.tsu_c)
        self.assertEqual(b, 1)
    
    def test_flesh_kincaid(self):
        a = self.fleshkinc(self.ts_s)
        self.assertEqual(a, 48.223888888888894)
        b = self.fleshkinc(self.ts_c)
        self.assertEqual(b, 3.655625000000015)

    def test_coleman_liau(self):
        a = self.colemanliau(self.ts_s)
        self.assertEqual(a, 10.614444444444441)
        b = self.colemanliau(self.ts_c)
        self.assertEqual(b, 17.70125)

    def test_SMOG(self):
        a = self.smog(self.ts_s)
        self.assertEqual(a, 15.363327528659473)
        b = self.smog(self.ts_c)
        self.assertEqual(b, 29.372789771779903)

    def test_ARI(self):
        a = self.ari(self.ts_s)
        self.assertEqual(a, 11.131166666666665)
        b = self.ari(self.ts_c)
        self.assertEqual(b, 19.224249999999998)

    def test_syntax(self):
        a = self.syntaxcompl(self.ts_s, self.tsu_s)
        self.assertEqual(a, 0.15780000000000005)
        b = self.syntaxcompl(self.ts_c, self.tsu_c)
        self.assertEqual(b, 0.537974358974359)

class TestBase(unittest.TestCase):
    
    def setUp(self):
        self.ts_s = get_ts(SIMPLE_TEXT)
        self.ts_c = get_ts(COMPLEX_TEXT)
        self.tsu_s = get_tsu(SIMPLE_TEXT)
        self.tsu_c = get_tsu(COMPLEX_TEXT)

        self.NumWords = NumWords()
        self.num_words = get_num_words
        self.ASLw = ASLw()
        self.asl = get_asl_w
        self.DependencyDist = DependencyDist()
        self.dep_dist = get_dep_distance


    def test_NumWords(self):
        a = self.NumWords.compute(SIMPLE_TEXT)
        self.assertEqual(a, self.num_words(self.ts_s))
        b = self.NumWords.compute(COMPLEX_TEXT)
        self.assertEqual(b, self.num_words(self.ts_c))
    
    def test_ASLw(self):
        a = self.ASLw.compute(SIMPLE_TEXT)
        self.assertEqual(a, self.asl(self.ts_s))
        b = self.ASLw.compute(COMPLEX_TEXT)
        self.assertEqual(b, self.asl(self.ts_c))

    def test_DepDist(self):
        a = self.DependencyDist.compute(SIMPLE_TEXT)
        self.assertEqual(a, self.dep_dist(self.tsu_s))
        b = self.DependencyDist.compute(COMPLEX_TEXT)
        self.assertEqual(b, self.dep_dist(self.tsu_c))

class TestCalc(unittest.TestCase):

    def setUp(self):
        self.calc = Calc(None)
        self.output1 = self.calc(SIMPLE_TEXT)
        self.output2 = self.calc(COMPLEX_TEXT)
        self.compcalc = ComplexCalc(None)
        self.output3 = self.compcalc(SIMPLE_TEXT)
        self.output4 = self.compcalc(COMPLEX_TEXT)

    def test_Calc(self):
        for k in self.output1.keys():
            self.assertIn(k, CalcOutput.__annotations__)
        for k in self.output2.keys():
            self.assertIn(k, CalcOutput.__annotations__)
    
    def test_CompCalc(self):
        for k in self.output3.keys():
            self.assertIn(k, ComplexCalcOutput.__annotations__)
        for k in self.output4.keys():
            self.assertIn(k, ComplexCalcOutput.__annotations__)

if __name__ == '__main__':
    unittest.main(verbosity=2)