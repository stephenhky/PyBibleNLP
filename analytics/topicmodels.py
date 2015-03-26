__author__ = 'hok1'

from gensim import corpora
from gensim.models.tfidfmodel import TfidfModel
import vectorize.DocVectorization as dv

# abstract class
class TopicModeler:
    def __init__(self, num_topics=50, corpus=None, dictionary=None, stemfunc=lambda s: s, toweight=True):
        self.num_topics = num_topics
        self.corpus = corpus
        self.dictionary = dictionary
        self.stemfunc = stemfunc
        self.vectorizer = dv.DocVectorizer()
        self.toweight = toweight

    def loadCorpus(self, mmfile, dictfile):
        self.corpus = corpora.MmCorpus(mmfile)
        self.dictionary = corpora.Dictionary.load(dictfile)
        if self.toweight:
            self.tfidf = TfidfModel(self.corpus)

    def stringTopic(self, topicid):
        return map(lambda weighttoken: (weighttoken[0], self.dictionary[int(weighttoken[1])]),
                   self.model.show_topic(topicid))

    def numTopics(self):
        return self.model.num_topics

    # need to implement
    def trainModel(self):
        self.model = None