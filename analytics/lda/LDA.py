__author__ = 'hok1'

import numpy as np
from gensim.models.ldamodel import LdaModel
from gensim import corpora

class LatentDirichletAllocation:
    def __init__(self, num_topics=50, corpus=None, dictionary=None):
        self.num_topics = num_topics
        self.corpus = corpus
        self.dictionary = dictionary

    def loadCorpus(self, mmfile, dictfile):
        self.corpus = corpora.MmCorpus(mmfile)
        self.dictionary = corpora.Dictionary.load(dictfile)

    def trainLDAmodel(self):
        self.lda = LdaModel(self.corpus, num_topics=self.num_topics)