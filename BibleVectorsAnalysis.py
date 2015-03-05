__author__ = 'hok1'

import numpy as np
import BookAbbrDict as abbr

class BibleBookAnalysis:
    def __init__(self, npz_dir):
        self.npz_dir = npz_dir
        self.tokenVecs = self.preloadTokenVectors()

    def preloadTokenVectors(self):
        tokenVecs = {}
        for book in (abbr.otbookdict.keys()+abbr.ntbookdict.keys()):
            vecs = np.load(self.npz_dir+'/'+book+'.npz')
            vecs = vecs['arr_0']
            tokens = np.load(self.npz_dir+'/'+book+'.tkn')
            tokens = tokens['arr_0']
            for token, vec in zip(tokens, vecs):
                if not tokenVecs.has_key(token):
                    tokenVecs[token] = vec
        return tokenVecs

    def getBookTermMatrix(self, books):
        veclist = []
        for book in books:
            vecs = np.load(self.npz_dir+'/'+book+'.npz')
            vecs = vecs['arr_0']
            veclist += [sum(vecs)]
        doctermMatrix = np.matrix(np.array(veclist))
        return doctermMatrix

    def getTermBookMatrix(self, books):
        return np.transpose(self.getBookTermMatrix(books))


