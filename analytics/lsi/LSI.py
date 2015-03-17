__author__ = 'hok1'

from Bible.BibleExceptions import BibleException
import numpy as np
from scipy.spatial.distance import cosine

class TokenNotFoundException(BibleException):
    def __init__(self, token):
        self._message = 'Token ['+token+'] not found.'

class LatentSemanticIndexing:
    def __init__(self, npzdir='.', stemfunc=lambda s: s):
        self.npzdir = npzdir
        self.stemfunc = stemfunc

    def preloadTokens(self, books):
        self.tokenVecs = {}
        for book in books:
            tokens = np.load(self.npzdir+'/'+book+'.tkn')
            tokens = tokens['arr_0']
            for token in tokens:
                stemmedToken = self.stemfunc(token)
                if not self.tokenVecs.has_key(stemmedToken):
                    self.tokenVecs[stemmedToken] = None
        for token, idx in zip(self.tokenVecs.keys(), range(len(self.tokenVecs))):
            vec = np.zeros(len(self.tokenVecs))
            vec[idx] = 1
            self.tokenVecs[token] = vec

    def calculateTermDocumentMatrix(self, books):
        veclist = []
        self.books = books
        for book in self.books:
            tokens = np.load(self.npzdir+'/'+book+'.tkn')
            tokens = tokens['arr_0']
            vecs = map(lambda token: self.tokenVecs[self.stemfunc(token)], tokens)
            veclist += [sum(vecs)]
        self.termdocMatrix = np.transpose(np.matrix(np.array(veclist)))

    def runLSI(self, books, k=None):
        self.k = k
        self.calculateTermDocumentMatrix(books)
        self.U, self.s, self.V = np.linalg.svd(self.termdocMatrix, full_matrices=False)
        self.U = np.matrix(self.U)
        self.V = np.matrix(self.V)
        if k!=None:
            self.U = self.U[:,:k]
            self.s = self.s[:k]
            self.V = self.V[:k,:]

    def reduceRankVec(self, vec, toTranspose=True):
        nvec = np.transpose(vec) if toTranspose else vec
        return np.array(np.matrix(nvec)*self.U)*self.s

    def reduceTokenRankVec(self, token):
        try:
            vec = self.tokenVecs[self.stemfunc(token)]
        except KeyError:
            raise TokenNotFoundException(token)
        return self.reduceRankVec(vec, toTranspose=False)

    def queryDocs(self, queryToken):
        reducedRankVec = self.reduceTokenRankVec(queryToken)
        cosines = [(book, 1-cosine(reducedRankVec, self.reduceRankVec(self.termdocMatrix[:,id]))) for id, book in zip(range(len(self.books)), self.books)]
        cosines = sorted(cosines, key=lambda item: item[1], reverse=True)
        return cosines

    def topicVectorsIterator(self):
        for i in range(self.k):
            vecstr = ''
            for j, token in zip(range(self.U.shape[0]), self.tokenVecs.keys()):
                vecstr += ('+' if self.U[j,i]>0 else '')+str(self.U[j,i])+'*'+token
            yield (self.s[i], vecstr)

class LatentSemanticIndexingForContinuousVectors(LatentSemanticIndexing):
    def preloadTokens(self, books):
        self.tokenVecs = {}
        for book in books:
            vecs = np.load(self.npzdir+'/'+book+'.npz')
            vecs = vecs['arr_0']
            tokens = np.load(self.npzdir+'/'+book+'.tkn')
            tokens = tokens['arr_0']
            for token, vec in zip(tokens, vecs):
                normalizedToken = self.stemfunc(token)
                if not self.tokenVecs.has_key(normalizedToken):
                    self.tokenVecs[normalizedToken] = vec

# term-frequency functions
unaryTF = lambda f: 1 if f>0 else 0
rawTF = lambda f: f
lognormalTF = lambda f: 1+np.log(float(f))

# inverse-document-frequency functions
unaryIDF = lambda N, n: 1
invfreqIDF = lambda N, n: np.log(N/(1.+n))
invfreqsmoothIDF = lambda N, n: np.log(1.+N/float(n))
probinvfreqIDF = lambda N, n: np.log((N-n)/float(n))

class LSIWordCountTFIDF(LatentSemanticIndexing):
    def __init__(self, npzdir='.', stemfunc=lambda s: s, tf=rawTF, idf=invfreqIDF):
        LatentSemanticIndexing.__init__(self, npzdir=npzdir, stemfunc=stemfunc)
        self.tf = tf
        self.idf = idf

    def calculateTermDocumentMatrix(self, books):
        LatentSemanticIndexing.calculateTermDocumentMatrix(self, books)
        rawTermDocMatrix = self.termdocMatrix
        docfreq = np.sum(rawTermDocMatrix!=0, axis=1)
        self.termdocMatrix = np.array(self.tf(rawTermDocMatrix))*np.array(self.idf(rawTermDocMatrix.shape[1], docfreq))
