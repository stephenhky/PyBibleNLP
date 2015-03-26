__author__ = 'stephenhky'

from gensim.models import LsiModel
from analytics.topicmodels import TopicModeler

class LatentSemanticIndexing(TopicModeler):
    def trainModel(self):
        if self.toweight:
            self.model = LsiModel(self.tfidf[self.corpus], num_topics=self.num_topics)
        else:
            self.model = LsiModel(self.corpus, num_topics=self.num_topics)

    def queryDocs(self, queryToken):
        pass