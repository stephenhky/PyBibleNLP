__author__ = 'hok1'

from Bible.BibleExceptions import TokenNotFoundException
import argparse
import Bible.BookAbbrDict as abbr
import Bible.KJV.KJVBibleParser as kbp
import analytics.lsi.old.LSI as lsi
import analytics.stem.stemfuncs as stemfuncs


TFdict = {'rawTF': lsi.rawTF, 'unaryTF': lsi.unaryTF, 'lognormalTF': lsi.lognormalTF}
IDFdict = {'unaryIDF': lsi.unaryIDF, 'invfreqIDF': lsi.invfreqIDF, 'invfreqsmoothIDF': lsi.invfreqsmoothIDF,
           'probinvfreqIDF': lsi.probinvfreqIDF}

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
    stemfunc = stemfuncs.getstemfunc(args.stemmer)
    indexer = lsi.LSIWordCountTFIDFKJVTokens(npzdir=args.npzdir, stemfunc=stemfunc,
                                    tf=TFdict[args.tf], idf=IDFdict[args.idf])
    chapkeys = getChapKeys(args.kjvdir)
    indexer.preloadTokens(chapkeys)
    indexer.runLSI(chapkeys, k=args.k)
    return indexer

def promptflow(indexer, numChap):
    while True:
        topicword = raw_input('topic> ')
        if topicword!='':
            try:
                retrievedChapters = indexer.queryDocs(topicword)
                for bookchapter, cosine in retrievedChapters[:min(numChap, len(retrievedChapters))]:
                    book, chapidx = bookchapter.split('_')
                    chapidx = int(chapidx)
                    print abbr.getBookName(book)+', Chapter '+str(chapidx)+' : '+str(cosine)
            except TokenNotFoundException:
                print 'Topic word ['+topicword+'] not found!'
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