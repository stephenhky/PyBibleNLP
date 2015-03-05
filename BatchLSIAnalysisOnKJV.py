__author__ = 'stephenhky'

import BookAbbrDict as abbr
from scipy.spatial.distance import cosine
import argparse
import numpy as np
from BibleVectorsAnalysis import BibleBookAnalysis
import csv

def performLSIAnalysis(analyzer, books, outputfile):
    termdocMatrix = analyzer.getTermBookMatrix(books)
    U, s, V = np.linalg.svd(termdocMatrix, full_matrices=False)
    sorted_tokens = sorted(analyzer.tokenVecs.keys())

    writer = csv.writer(outputfile)
    writer.writerow(['ID']+sorted_tokens)
    for idx in range(len(s)):
        writer.writerow([idx]+[1-cosine(U[:, idx], analyzer.tokenVecs[token]) for token in sorted_tokens])
    outputfile.close()

def main():
    argv_parser = argparse.ArgumentParser(description='Analyzing bible books')
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