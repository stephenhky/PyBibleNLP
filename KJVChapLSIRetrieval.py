__author__ = 'hok1'

import Bible.BookAbbrDict as abbr
import Bible.KJV.KJVBibleParser as kbp
from Bible.BibleExceptions import BibleException
import analytics.lsi.LSI as lsi
import argparse
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

TFdict = {'rawTF': lsi.rawTF, 'unaryTF': lsi.unaryTF, 'lognormalTF': lsi.lognormalTF}
IDFdict = {'unaryIDF': lsi.unaryIDF, 'invfreqIDF': lsi.invfreqIDF, 'invfreqsmoothIDF': lsi.invfreqsmoothIDF,
           'probinvfreqIDF': lsi.probinvfreqIDF}

class NoStemmerException(BibleException):
    def __init__(self):
        self._message = 'No such stemmer!'

def getArgvParser():
    argvParser = argparse.ArgumentParser(description='Perform retrieval on chapters in KJV Bible with latent semantic indexing (LSI)')
    argvParser.add_argument('npzdir', help='directory of where the tokens are stored in ".tkn" format')
    argvParser.add_argument('kjvdir', help='directory where the KJV text (kjvdat.txt) is stored')
    argvParser.add_argument('--stemmer', help='stemmer', default='')
    argvParser.add_argument('--tf', help='TF (total frequency) function ('+','.join(TFdict.keys())+')', default='rawTF')
    argvParser.add_argument('--idf', help='IDF (inverse document frequency) function ('+','.join(IDFdict.keys())+')', default='invfreqIDF')
    argvParser.add_argument('--k', help='reduced dimension of vectors', type=int, default=50)
    argvParser.add_argument('--numChap', help='number of chapters to displayed in each retrieval', type=int, default=10)
    return argvParser

def getChapKeys(kjv_dir):
    kjvParser = kbp.KJVParser(kjv_dir)
    chapKeys = [book+'_'+str(chapidx) for book, chapidx in kjvParser.chapIterator(abbr.otbookdict.keys()+abbr.ntbookdict.keys())]
    return chapKeys

def getLSIAnalyzer(args):
    if args.stemmer=='':
        stemfunc = lambda s: s
    elif args.stemmer=='porter':
        porterStemmer = PorterStemmer()
        stemfunc = lambda s: porterStemmer.stem(s)
    elif args.stemmer=='lancaster':
        lancasterStemmer = LancasterStemmer()
        stemfunc = lambda s: lancasterStemmer.stem(s)
    elif args.stemmer=='wordnetLemmatizer':
        lemmatizer = WordNetLemmatizer()
        stemfunc = lambda s: str(min(lemmatizer.lemmatize(s, 'v'), lemmatizer.lemmatize(s, 'n'),
                                     key=lambda st: len(st))
        )
    else:
        raise NoStemmerException()
    indexer = lsi.LSIWordCountTFIDF(npzdir=args.npzdir, stemfunc=stemfunc,
                                    tf=TFdict[args.tf], idf=IDFdict[args.idf])
    chapkeys = getChapKeys(args.kjvdir)
    indexer.preloadTokens(chapkeys)
    indexer.runLSI(chapkeys, k=args.k)
    return indexer

def promptflow(indexer, numChap):
    while True:
        topicword = raw_input('topic> ')
        if topicword!='':
            retrievedChapters = indexer.queryDocs(topicword)
            for bookchapter, cosine in retrievedChapters[:min(numChap, len(retrievedChapters))]:
                book, chapidx = bookchapter.split('_')
                chapidx = int(chapidx)
                print abbr.getBookName(book)+', Chapter '+str(chapidx)+' : '+str(cosine)
        else:
            break

if __name__=='__main__':
    argvParser = getArgvParser()
    args = argvParser.parse_args()
    print 'Preparing analyzer...'
    indexer = getLSIAnalyzer(args)
    print 'Type a topic word that you want to retrieve and press ENTER/RETURN.'
    print 'Or simply press ENTER/RETURN to exit.'
    promptflow(indexer, args.numChap)