__author__ = 'stephenhky'

from gensim import corpora
import vectorize.DocVectorization as dv

class LatentSemanticIndexing:
    def __init__(self, num_topics=50, corpus=None, dictionary=None, stemfunc=lambda s: s):
        self.num_topics = num_topics
        self.corpus = corpus
        self.dictionary = dictionary
        self.stemfunc = stemfunc
        self.vectorizer = dv.DocVectorizer()

    def loadCorpus(self, mmfile, dictfile):
        self.corpus = corpora.MmCorpus(mmfile)
        self.dictionary = corpora.Dictionary.load(dictfile)