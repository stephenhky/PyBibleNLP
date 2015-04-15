__author__ = 'hok1'

import argparse
import BibleTMChapRetrieval as retrieval

def getArgvParser():
    argvParser = argparse.ArgumentParser(description='Perform retrieval on chapters in KJV Bible with latent semantic indexing (LSI)')
    argvParser.add_argument('mmcorpusfile', help='path of the MM corpus')
    argvParser.add_argument('dictfile', help='path of the dictionary')
    argvParser.add_argument('chapkeysfile', help='file that store the list of bible chapters')
    argvParser.add_argument('model', help='model (LDA or LSI)')
    argvParser.add_argument('modeloutputfile', help='path of the .model file')
    argvParser.add_argument('--stemmer', help='stemmer', default='')
    argvParser.add_argument('--tfidf', help='implement tf-idf weighting', action='store_false', default=False)
    argvParser.add_argument('--k', help='number of topics', type=int, default=50)
    return argvParser

if __name__=='__main__':
    argvParser = getArgvParser()
    args = argvParser.parse_args()
    print 'Preparing analyzer...'
    modeler = retrieval.getAnalyzer(args)
    print 'Saving model...'
    modeler.model.save(args.modeloutputfile)