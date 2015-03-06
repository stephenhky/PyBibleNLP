__author__ = 'stephenhky'

import argparse
import csv

from scipy.spatial.distance import cosine
import numpy as np

from Bible import BookAbbrDict as abbr
from vectorize.BibleVectorsAnalysis import BibleBookAnalysis


def performLSIAnalysis(analyzer, books, outputfile):
    termdocMatrix = analyzer.getTermBookMatrix(books)
    U, s, V = np.linalg.svd(termdocMatrix, full_matrices=False)
    sorted_tokens = sorted(analyzer.tokenVecs.keys())

    writer = csv.writer(outputfile)
    writer.writerow(['token']+range(len(s)))
    for token in sorted_tokens:
        writer.writerow([token]+[1-cosine(U[:, idx], analyzer.tokenVecs[token]) for idx in range(len(s))])
    outputfile.close()

def main():
    argv_parser = argparse.ArgumentParser(description='Analyzing Bible books')
    argv_parser.add_argument('npz_dir', help='token information directory')
    argv_parser.add_argument('analysis_pathprefix', help='prefix of the path of output analyses')
    args = argv_parser.parse_args()

    analyzer = BibleBookAnalysis(args.npz_dir)

    performLSIAnalysis(analyzer, abbr.otbookdict.keys()+abbr.ntbookdict.keys(),
                       open(args.analysis_pathprefix+'_WholeBible.csv', 'wb'))
    performLSIAnalysis(analyzer, abbr.otbookdict.keys(), open(args.analysis_pathprefix+'_OldTestament.csv', 'wb'))
    performLSIAnalysis(analyzer, abbr.ntbookdict.keys(), open(args.analysis_pathprefix+'_NewTestament.csv', 'wb'))

if __name__ == '__main__':
    main()