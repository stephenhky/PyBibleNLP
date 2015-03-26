__author__ = 'hok1'

from gensim.models.ldamodel import LdaModel
from analytics.topicmodels import TopicModeler

class LatentDirichletAllocation(TopicModeler):
    def trainModel(self):
        if self.toweight:
            self.model = LdaModel(self.tfidf[self.corpus], num_topics=self.num_topics)
        else:
            self.model = LdaModel(self.corpus, num_topics=self.num_topics)

    def queryDocTopics(self, docstr):
        return self.model[ self.dictionary.doc2bow( self.vectorizer.tokenizeDoc(docstr))]

