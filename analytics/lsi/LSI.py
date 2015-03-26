__author__ = 'stephenhky'

from gensim.models import LsiModel
from gensim import similarities
from analytics.topicmodels import TopicModeler

class LatentSemanticIndexing(TopicModeler):
    def trainModel(self):
        if self.toweight:
            self.model = LsiModel(self.tfidf[self.corpus], num_topics=self.num_topics)
            self.index = similarities.MatrixSimilarity(self.model[self.tfidf[self.corpus]])
        else:
            self.model = LsiModel(self.corpus, num_topics=self.num_topics)
            self.index = similarities.MatrixSimilarity(self.model[self.corpus])


