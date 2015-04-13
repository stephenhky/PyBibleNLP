__author__ = 'hok1'

from collections import defaultdict
from xml.dom.minidom import parse

from Bible import BookAbbrDict as abbr
from Bible.BibleParser import BibleParser
from Bible.BibleExceptions import NoBibleBookException

class KJVParser(BibleParser):

    def parseBook(self, bookabbr):
        filepath = self.bookdir+'/'+bookabbr+'.xml'
        self.currentbook = bookabbr
        self.bookcontent = defaultdict(lambda : {})
        try:
            abbr.getBookName(bookabbr)
        except KeyError:
            raise NoBibleBookException(bookabbr)

        # not finished, include chapters
        dom = parse(open(filepath, 'rb'))
        for item in dom.getElementsByTagName('verse-unit'):
            nodenames = map(lambda node: node.nodeName, item.childNodes)
            versenum = -1
            versetext = ''
            for posid, nodename in zip(range(len(nodenames)), nodenames):
                if nodename == 'verse-num':
                    versenum = int(item.childNodes[posid].nodeValue)
                if nodename == '#text':
                    versetext = item.childNodes[posid].nodeValue.strip()
            if versenum > 0:
                self.bookcontent[chap][versenum] = versetext