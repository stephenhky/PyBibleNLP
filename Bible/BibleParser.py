__author__ = 'hok1'

from Bible import BookAbbrDict as abbr
from Bible.BibleExceptions import BibleException, InvalidBibleChapterException, InvalidBibleLocationException

class BibleParser:
    def __init__(self):
        self.currentbook = None

    # needs to be implemented
    def parseBook(self, bookabbr):
        pass

    def getNumChapters(self, bookabbr):
        if bookabbr != self.currentbook:
            self.parseBook(bookabbr)
        return len(self.bookcontent)

    def getNumVerses(self, bookabbr, chap):
        if bookabbr != self.currentbook:
            self.parseBook(bookabbr)
        if chap > self.getNumChapters(bookabbr):
            raise InvalidBibleChapterException(bookabbr, chap)
        return max(self.bookcontent[chap].keys())

    def retrieveVerse(self, bookabbr, chap, verse):
        if bookabbr != self.currentbook:
            self.parseBook(bookabbr)
        try:
            scripture = self.bookcontent[chap][verse]
        except KeyError:
            raise InvalidBibleLocationException(bookabbr, chap, verse)
        return scripture

    def retrieveVersesIterator(self, bookabbr, startChap, startVerse, endChap, endVerse):
        # validation
        if startChap > endChap or (startChap==endChap and startVerse>endVerse):
            raise BibleException('Wrong chapter sequence: '+str(startChap)+'>'+str(endChap))
        numChaps = self.getNumChapters(bookabbr)
        if startChap > numChaps:
            raise InvalidBibleChapterException(bookabbr, startChap)
        if startVerse > self.getNumVerses(bookabbr, startChap):
            raise InvalidBibleLocationException(bookabbr, startChap, startVerse)

        # iterator
        for chap in range(startChap, min(endChap, numChaps)+1):
            startingVerse = startVerse if chap==startChap else 1
            numVerses = self.getNumVerses(bookabbr, chap)
            endingVerse = endVerse if chap==endChap and numVerses>=endVerse else numVerses
            for verse in range(startingVerse, endingVerse+1):
                try:
                    text = self.retrieveVerse(bookabbr, chap, verse)
                except InvalidBibleLocationException:
                    text = ''
                yield (bookabbr, chap, verse, text)

    def retrieveVerses(self, bookabbr, startChap, startVerse, endChap, endVerse):
        versesIterator = self.retrieveVersesIterator(bookabbr, startChap, startVerse, endChap, endVerse)
        return ' '.join([verseTuple[3] for verseTuple in versesIterator])

    def chapIterator(self, books):
        for bookabbr in books:
            for chapIdx in range(1, self.getNumChapters(bookabbr)+1):
                yield (bookabbr, chapIdx)

    def otChapters(self):
        return self.chapIterator(abbr.otbookdict.keys())

    def ntChapters(self):
        return self.chapIterator(abbr.ntbookdict.keys())
