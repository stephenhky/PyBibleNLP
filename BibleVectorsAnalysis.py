__author__ = 'hok1'

import numpy as np
import BookAbbrDict as abbr
from scipy.spatial.distance import cosine
import argparse

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

def performLSIAnalysis(npz_dir):
    analyzer = BibleBookAnalysis(npz_dir)
    termdocMatrix = analyzer.getTermBookMatrix(abbr.otbookdict.keys()+abbr.ntbookdict.keys())
    U, s, V = np.linalg.svd(termdocMatrix, full_matrices=False)
    while True:
        idx = int(raw_input('Index = ? '))
        relevances = [(token, 1-cosine(U[:, idx], analyzer.tokenVecs[token])) for token in analyzer.tokenVecs.keys()]
        relevances = sorted(relevances, key=lambda item: item[1], reverse=True)
        for relevance in relevances[:30]:
            print relevance

if __name__ == '__main__':
    argv_parser = argparse.ArgumentParser(description='Analyzing bible books')
    argv_parser.add_argument('npz_dir', help='token information directory')
    args = argv_parser.parse_args()
    performLSIAnalysis(args.npz_dir)
