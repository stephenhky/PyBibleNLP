__author__ = 'hok1'

from gensim.models.ldamodel import LdaModel
from gensim import corpora
import vectorize.DocVectorization as dv

class LatentDirichletAllocation:
    def __init__(self, num_topics=50, corpus=None, dictionary=None, stemfunc=lambda s: s):
        self.num_topics = num_topics
        self.corpus = corpus
        self.dictionary = dictionary
        self.stemfunc = stemfunc
        self.vectorizer = dv.DocVectorizer()

    def loadCorpus(self, mmfile, dictfile):
        self.corpus = corpora.MmCorpus(mmfile)
        self.dictionary = corpora.Dictionary.load(dictfile)

    def trainLDAmodel(self):
        self.lda = LdaModel(self.corpus, num_topics=self.num_topics)

    def queryDocTopics(self, docstr):
        return self.lda[ self.dictionary.doc2bow( self.vectorizer.tokenizeDoc(docstr))]

    def stringTopic(self, topicid):
        return map(lambda weighttoken: (weighttoken[0], self.dictionary[int(weighttoken[1])]),
                   self.lda.show_topic(topicid))

    def numTopics(self):
        return self.lda.num_topics