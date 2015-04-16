__author__ = 'hok1'

from collections import defaultdict
from xml.dom.minidom import parse
import re

from Bible import BookAbbrDict as abbr
from Bible.BibleParser import BibleParser
from Bible.BibleExceptions import NoBibleBookException, BibleException

class ESVParser(BibleParser):
    def __init__(self, bookdir, chaptuples=None):
        BibleParser.__init__(self)
        self.bookdir = bookdir
        self.bookcontent = {}
        self.chaptuples = chaptuples

    def parseBook(self, bookabbr):
        if self.chaptuples == None:
            raise BibleException('No chaptuples defined.')

        self.currentbook = bookabbr
        self.bookcontent = defaultdict(lambda : {})
        try:
            abbr.getBookName(bookabbr)
        except KeyError:
            raise NoBibleBookException(bookabbr)

        bookchaptuples = filter(lambda t: t[0]==bookabbr, self.chaptuples)
        for bk, chap in bookchaptuples:
            filepath = self.bookdir+'/'+bookabbr+'_'+str(chap)+'.xml'
            dom = parse(open(filepath, 'rb'))
            for item in dom.getElementsByTagName('verse-unit'):
                nodenames = map(lambda node: node.nodeName, item.childNodes)
                versenum = -1
                versetext = ''
                for posid, nodename in zip(range(len(nodenames)), nodenames):
                    if nodename == 'verse-num':
                        versenum = int(item.childNodes[posid].firstChild.nodeValue)
                    if nodename == '#text':
                        versetext += ' '+item.childNodes[posid].nodeValue.strip()
                    if nodename == 'woc':
                        versetext += ' '+item.childNodes[posid].firstChild.nodeValue.strip()
                if versenum > 0:
                    self.bookcontent[chap][versenum] = re.sub('\\s+', ' ', versetext)

    def retrieveVersesIterator(self, bookabbr, startChap, startVerse, endChap, endVerse):
        if bookabbr != self.currentbook:
            self.parseBook(bookabbr)
        return BibleParser.retrieveVersesIterator(self, bookabbr, startChap, startVerse, endChap, endVerse)