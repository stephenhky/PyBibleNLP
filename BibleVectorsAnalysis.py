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
                if vec != None and (not tokenVecs.has_key(token)):
                    tokenVecs[token] = vec
        return tokenVecs

    def getDocTermMatrix(self, books):
        veclist = []
        for book in books:
            vecs = np.load(self.npz_dir+'/'+book+'.npz')
            vecs = vecs['arr_0']
            #tokens = np.load(self.npz_dir+'/'+book+'.tkn')
            #tokens = tokens['arr_0']
            #filteredPairs = filter(lambda pair: pair[1]!=None, zip(tokens, vecs))
            #vecs = map(lambda pair: pair[1], filteredPairs)
            #tokens = map(lambda pair: pair[0], filteredPairs)
            veclist += [sum(vecs)]
        doctermMatrix = np.matrix(np.array(veclist))
        return doctermMatrix

    def getTermDocMatrix(self, books):
        return np.transpose(self.getDocTermMatrix(books))