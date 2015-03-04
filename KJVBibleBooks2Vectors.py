__author__ = 'hok1'

import KJVBibleParser
import DocVectorization
import BookAbbrDict
import numpy as np
import argparse

def argument_parser():
    argv_parser = argparse.ArgumentParser(description='Parsing the KJV Books into vectors using word2vec')
    argv_parser.add_argument('kjv_dir', help='directory of the KJV Books')
    argv_parser.add_argument('output_dir', help='output directory')
    argv_parser.add_argument('word2vec_model', help='word2vec model path')
    return argv_parser

if __name__ == '__main__':
    argv_parser = argument_parser()
    args = argv_parser.parse_args()

    parser = KJVBibleParser.KJVParser(args.kjv_dir)
    vectorizer = DocVectorization.DocVectorizer(args.word2vec_model)

    for bookabbr in BookAbbrDict.otbookdict.keys() + BookAbbrDict.ntbookdict.keys():
        print 'Calculating '+BookAbbrDict.getBookName(bookabbr)

        print '  Retrieving vectors...'
        booktext = parser.retrieveVerses(bookabbr, 1, 1, 200, 1)
        tokens, vectors = vectorizer.retrieveDocVectors(booktext)

        print '   Writing to files...'
        outputtokenfile = open(args.output_dir+'/'+bookabbr+'.tkn', 'wb')
        np.savez(outputtokenfile, tokens)
        outputnpzfile = open(args.output_dir+'/'+bookabbr+'.npz', 'wb')
        np.savez(outputnpzfile, vectors)

    print 'Finished.'