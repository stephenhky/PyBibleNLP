__author__ = 'hok1'

import argparse
import time
import pickle

import Bible.KJV.KJVBibleParser as kbp
import Bible.ESV.ESVBibleParser as ebp
from vectorize import DocVectorization
from Bible import BookAbbrDict as abbr
from gensim import corpora
import analytics.stemfuncs as stemfuncs

def argument_parser():
    argv_parser = argparse.ArgumentParser(description='Parsing the bible (KJV/ESV) chapters into gensim corpus')
    argv_parser.add_argument('text_dir', help='directory of the books')
    argv_parser.add_argument('output_dir', help='output directory')
    argv_parser.add_argument('chaptuples', help='path of chaptuples pickle file')
    argv_parser.add_argument('translation', help='translation (KJV/ESV)')
    argv_parser.add_argument('--stemmer', help='stemmer (porter/stemmer/wordnetLemmatizer)', default='')
    return argv_parser

if __name__ == '__main__':
    argparser = argument_parser()
    args = argparser.parse_args()

    print 'Initializing....'
    vectorizer = DocVectorization.DocVectorizer()
    chaptuples = pickle.load(open(args.chaptuples, 'rb'))
    if args.translation.lower() == 'kjv':
        parser = kbp.KJVParser(args.text_dir, chaptuples=chaptuples)
    elif args.translation.lower() == 'esv':
        parser = ebp.ESVParser(args.text_dir, chaptuples=chaptuples)

    starttime = time.time()

    print 'Parsing the Bible...'
    documents = [parser.retrieveVerses(book, chapidx, 1, chapidx, parser.getNumVerses(book, chapidx)) for book, chapidx in parser.chapIterator(abbr.otbookdict.keys()+abbr.ntbookdict.keys())]
    print 'Building gensim corpus'
    dictionary, corpus = vectorizer.retrieveGensimCorpora(documents, stemfunc=stemfuncs.getstemfunc(args.stemmer))

    endtime = time.time()
    print 'Finished.'
    print 'Time elapsed = ', (endtime-starttime), ' sec'

    dictionary.save(args.output_dir+'/'+args.translation.lower()+'dictionary.dict')
    corpora.MmCorpus.serialize(args.output_dir+'/'+args.translation.lower()+'corpus.mm', corpus)
