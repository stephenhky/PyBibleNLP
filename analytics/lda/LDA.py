__author__ = 'hok1'

from gensim.models.ldamodel import LdaModel
from analytics.topicmodels import TopicModeler
from gensim import similarities

class LatentDirichletAllocation(TopicModeler):
    def trainModel(self):
        if self.toweight:
            self.model = LdaModel(self.tfidf[self.corpus], num_topics=self.num_topics)
            self.index = similarities.MatrixSimilarity(self.model[self.tfidf[self.corpus]])
        else:
            self.model = LdaModel(self.corpus, num_topics=self.num_topics)
            self.index = similarities.MatrixSimilarity(self.model[self.corpus])

    def loadModel(self, modelfile):
        self.model = LdaModel.load(modelfile)
        if self.toweight:
            self.index = similarities.MatrixSimilarity(self.model[self.tfidf[self.corpus]])
        else:
            self.index = similarities.MatrixSimilarity(self.model[self.corpus])

    def queryDocTopics(self, docstr):
        if self.toweight:
            return self.model[ self.tfidf[self.dictionary.doc2bow( self.vectorizer.tokenizeDoc(docstr))]]
        else:
            return self.model[ self.dictionary.doc2bow( self.vectorizer.tokenizeDoc(docstr))]

    def __str__(self):
        return 'Latent Dirichlet Allocation (LDA)'