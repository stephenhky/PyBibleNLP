__author__ = 'hok1'

from Bible.BibleExceptions import BibleException
import numpy as np
from scipy.spatial.distance import cosine

class TokenNotFoundException(BibleException):
    def __init__(self, token):
        self._message = 'Token ['+token+'] not found.'

class LatentSemanticIndexing:
    def __init__(self, npzdir='.'):
        self.npzdir = npzdir

    def preloadTokens(self, books):
        self.tokenVecs = {}
        for book in books:
            vecs = np.load(self.npzdir+'/'+book+'.npz')
            vecs = vecs['arr_0']
            tokens = np.load(self.npzdir+'/'+book+'.tkn')
            tokens = tokens['arr_0']
            for token, vec in zip(tokens, vecs):
                if not self.tokenVecs.has_key(token):
                    self.tokenVecs[token] = vec

    def runLSI(self, books):
        veclist = []
        for book in books:
            vecs = np.load(self.npzdir+'/'+book+'.npz')
            vecs = vecs['arr_0']
            veclist += [sum(vecs)]
        self.termdocMatrix = np.transpose(np.matrix(np.array(veclist)))
        self.U, self.s, self.V = np.linalg.svd(self.termdocMatrix, full_matrices=False)
        self.U = np.matrix(self.U)
        self.V = np.matrix(self.V)

    def reduceRankVec(self, token):
        try:
            vec = self.tokenVecs[token]
        except KeyError:
            raise TokenNotFoundException(token)
        return np.array(np.matrix(vec)*self.U)*self.s

    def query(self, queryToken):
        reducedRankVec = self.reduceRankVec(queryToken)
        cosines = [(token, 1-cosine(reducedRankVec, self.reduceRankVec(token))) for token in self.tokenVecs.keys()]
        cosines = sorted(cosines, key=lambda item: item[1], reverse=True)
        return cosines