__author__ = 'stephenhky'

import argparse

from scipy.spatial.distance import cosine
import numpy as np

from bible import BookAbbrDict as abbr
from vectorize.BibleVectorsAnalysis import BibleBookAnalysis


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