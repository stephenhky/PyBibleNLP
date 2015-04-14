__author__ = 'hok1'

from collections import defaultdict
from xml.dom.minidom import parse

from Bible import BookAbbrDict as abbr
from Bible.BibleParser import BibleParser
from Bible.BibleExceptions import NoBibleBookException, BibleException

class ESVParser(BibleParser):

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
                        versetext += item.childNodes[posid].nodeValue.strip()
                if versenum > 0:
                    self.bookcontent[chap][versenum] = versetext