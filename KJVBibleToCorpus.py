__author__ = 'hok1'

import argparse
import time
import pickle
import Bible.KJV.KJVBibleParser as kbp
from vectorize import DocVectorization
from Bible import BookAbbrDict as abbr
from gensim import corpora

def argument_parser():
    argv_parser = argparse.ArgumentParser(description='Parsing the KJV chapters into gensim corpus')
    argv_parser.add_argument('kjv_dir', help='directory of the KJV Books')
    argv_parser.add_argument('output_dir', help='output directory')
    return argv_parser

if __name__ == '__main__':
    argparser = argument_parser()
    args = argparser.parse_args()

    print 'Initializing....'
    vectorizer = DocVectorization.DocVectorizer()
    parser = kbp.KJVParser(args.kjv_dir)

    starttime = time.time()

    print 'Retrieving chapters...'
    chaptuples = [(book, chapidx) for book, chapidx in parser.chapIterator(abbr.otbookdict.keys()+abbr.ntbookdict.keys())]
    print 'Parsing the Bible...'
    documents = [parser.retrieveVerses(book, chapidx, 1, chapidx, parser.getNumVerses(book, chapidx)) for book, chapidx in parser.chapIterator(abbr.otbookdict.keys()+abbr.ntbookdict.keys())]
    print 'Building gensim corpus'
    dictionary, corpus = vectorizer.retrieveGensimCorpora(documents)

    endtime = time.time()
    print 'Finished.'
    print 'Time elapsed = ', (endtime-starttime), ' sec'

    dictionary.save(args.output_dir+'/kjvdictionary.dict')
    corpora.MmCorpus.serialize(args.output_dir+'/kjvcorpus.mm', corpus)
    chaptuplepickle = open(args.output_dir+'/chaptuples.pickle', 'wb')
    pickle.dump(chaptuples, chaptuplepickle)
    chaptuplepickle.close()