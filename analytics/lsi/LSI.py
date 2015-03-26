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

    def queryDocs(self, queryToken):
        if self.toweight:
            reducedvec = self.model[ self.tfidf[self.dictionary.doc2bow( self.vectorizer.tokenizeDoc(queryToken))]]
        else:
            reducedvec = self.model[ self.dictionary.doc2bow( self.vectorizer.tokenizeDoc(queryToken))]
        sims = self.index[reducedvec]
        simtuples = zip(range(len(sims)), sims) if self.doctuples==None else zip(self.doctuples, sims)
        simtuples = sorted(simtuples, key=lambda item: item[1], reverse=True)
        return simtuples
