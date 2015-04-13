__author__ = 'hok1'

import Bible.BookAbbrDict as abbr
import Bible.ESV.ESVOnlineBibleParser as esvparse
import argparse
import pickle

def getArgParser():
    argparser = argparse.ArgumentParser(description='Parse ESV Bible from API and save it')
    argparser.add_argument('key', help='Key')
    argparser.add_argument('output_path', help='Output Path')
    argparser.add_argument('chapkey', help='Path of chapkey.pickle')
    return argparser

if __name__ == '__main__':
    argparser = getArgParser()
    args = argparser.parse_args()
    output_dir = args.output_path
    esvkey = args.key

    parser = esvparse.ESVOnlineParser(esvkey)

    for bookabbr, chapidx in pickle.load(open(args.chapkey, 'rb')):
        print 'Retrieving '+abbr.getBookName(bookabbr)+' '+str(chapidx)
        response = parser.query(bookabbr, chapidx)
        print '\tWriting...'
        parser.save_url(output_dir+'/'+bookabbr+'_'+str(chapidx)+'.xml', response)