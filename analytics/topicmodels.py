__author__ = 'hok1'

from gensim import corpora
from gensim.models.tfidfmodel import TfidfModel
import vectorize.DocVectorization as dv
import pickle

# abstract class
class TopicModeler:
    def __init__(self, num_topics=50, corpus=None, dictionary=None, doctuples=None, stemfunc=lambda s: s, toweight=True):
        self.num_topics = num_topics
        self.corpus = corpus
        self.dictionary = dictionary
        self.doctuples = doctuples
        self.stemfunc = stemfunc
        self.vectorizer = dv.DocVectorizer()
        self.toweight = toweight

    def loadCorpus(self, mmfile, dictfile, doctuplesfile=None):
        self.corpus = corpora.MmCorpus(mmfile)
        self.dictionary = corpora.Dictionary.load(dictfile)
        if doctuplesfile!=None:
            self.doctuples = pickle.load(open(doctuplesfile, 'rb'))
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
        self.index = None

    def queryDocs(self, queryToken):
        if self.toweight:
            reducedvec = self.model[ self.tfidf[self.dictionary.doc2bow( self.vectorizer.tokenizeDoc(queryToken))]]
        else:
            reducedvec = self.model[ self.dictionary.doc2bow( self.vectorizer.tokenizeDoc(queryToken))]
        sims = self.index[reducedvec]
        simtuples = zip(range(len(sims)), sims) if self.doctuples==None else zip(self.doctuples, sims)
        simtuples = sorted(simtuples, key=lambda item: item[1], reverse=True)
        return simtuples