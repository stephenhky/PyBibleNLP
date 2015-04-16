__author__ = 'hok1'

from Bible.BibleParser import BibleParser
from BibleMongoDB import bibledb

class BibleMongoDBExtractor(BibleParser):
    def __init__(self, translation):
        BibleParser.__init__(self)
        self.transver = translation

    def getNumChapters(self, bookabbr):
        return len(set([item['chap'] for item in bibledb[self.transver].find({'book': bookabbr})]))

    def getNumVerses(self, bookabbr, chap):
        return max(set([item['verse'] for item in bibledb[self.transver].find({'book': bookabbr, 'chap': chap})]))

    def retrieveVerse(self, bookabbr, chap, verse):
        texts = [item['text'] for item in bibledb[self.transver].find({'book': bookabbr, 'chap': chap, 'verse': verse})]
        return '' if len(texts)==0 else texts[0]
