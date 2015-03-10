__author__ = 'hok1'

import argparse
import time

import numpy as np

from Bible.KJV import KJVBibleParser
from vectorize import DocVectorization
from Bible import BookAbbrDict


def argument_parser():
    argv_parser = argparse.ArgumentParser(description='Parsing the KJV chapters into vectors using word2vec')
    argv_parser.add_argument('kjv_dir', help='directory of the KJV Books')
    argv_parser.add_argument('output_dir', help='output directory')
    argv_parser.add_argument('word2vec_model', help='word2vec model path')
    return argv_parser

if __name__ == '__main__':
    argv_parser = argument_parser()
    args = argv_parser.parse_args()

    starttime = time.time()
    print 'Initialzing parser'
    parser = KJVBibleParser.KJVParser(args.kjv_dir)
    print 'Loading word2vec model'
    vectorizer = DocVectorization.DocVectorizer(args.word2vec_model)

    for bookabbr in BookAbbrDict.otbookdict.keys() + BookAbbrDict.ntbookdict.keys():
        for chapIdx in range(1, parser.getNumChapters(bookabbr)+1):
            keystr = bookabbr+'_'+str(chapIdx)
            print 'Calculating '+ BookAbbrDict.getBookName(bookabbr) + ' ' + str(chapIdx) + ' (' + keystr + ')'

            print '  Retrieving vectors...'
            booktext = parser.retrieveVerses(bookabbr, chapIdx, 1, chapIdx, parser.getNumVerses(bookabbr, chapIdx))
            tokens, vectors = vectorizer.retrieveDocVectors(booktext)

            print '  Writing to files...'
            outputtokenfile = open(args.output_dir+'/'+keystr+'.tkn', 'wb')
            np.savez(outputtokenfile, tokens)
            outputnpzfile = open(args.output_dir+'/'+keystr+'.npz', 'wb')
            np.savez(outputnpzfile, vectors)

    endtime = time.time()
    print 'Finished.'
    print 'Time elapsed = ', (endtime-starttime), ' sec'

    print 'Finished.'