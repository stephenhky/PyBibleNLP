__author__ = 'hok1'

import argparse
import BibleMongoDB as bdbdriver
import Bible.KJV.KJVBibleParser as kbp
import Bible.ESV.ESVBibleParser as ebp
from Bible.BibleExceptions import NoBibleTranslationException, InvalidBibleLocationException
import pickle

def argument_parser():
    argv_parser = argparse.ArgumentParser(description='Parsing the bible chapters into mongoDB (PyBibleNLP)')
    argv_parser.add_argument('text_dir', help='directory of the books')
    argv_parser.add_argument('chaptuples', help='path of chaptuples pickle file')
    argv_parser.add_argument('translation', help='translation')
    return argv_parser

if __name__ == '__main__':
    argparser = argument_parser()
    args = argparser.parse_args()

    chaptuples = pickle.load(open(args.chaptuples, 'rb'))

    transver = args.translation.upper()
    if transver == 'KJV':
        parser = kbp.KJVParser(args.text_dir, chaptuples=chaptuples)
    elif transver == 'ESV':
        parser = ebp.ESVParser(args.text_dir, chaptuples=chaptuples)
    else:
        raise NoBibleTranslationException(transver)

    db = bdbdriver.bibledb
    bibletranslation = db[transver]

    for bookabbr, chapidx in parser.chaptuples:
        numVerses = parser.getNumVerses(bookabbr, chapidx)
        for verseidx in range(1, numVerses+1):
            try:
                verseitem = {'book': bookabbr, 'chap': chapidx, 'verse': verseidx,
                             'text': parser.retrieveVerse(bookabbr, chapidx, verseidx)}
            except InvalidBibleLocationException:
                continue
            result = bibletranslation.insert(verseitem)
