__author__ = 'hok1'

import BookAbbrDict as abbr
from collections import defaultdict
import re
from BibleExceptions import BibleException, InvalidBibleChapterException, InvalidBibleLocationException, NoBibleBookException

bknameref = {
    "Genesis": "gen",
    "Exodus": "exo",
    "Leviticus": "lev",
    "Numbers": "num",
    "Deuteronomy": "deu",
    "Joshua": "jos",
    "Judges": "jdg",
    "Ruth": "rut",
    "1 Samuel": "sa1",
    "2 Samuel": "sa2",
    "1 Kings": "kg1",
    "2 Kings": "kg2",
    "1 Chronicles": "ch1",
    "2 Chronicles": "ch2",
    "Ezra": "ezr",
    "Nehemiah": "neh",
    "Esther": "est",
    "Job": "job",
    "Psalms": "psa",
    "Proverbs": "pro",
    "Ecclesiastes": "ecc",
    "Song of Solomon": "sol",
    "Isaiah": "isa",
    "Jeremiah": "jer",
    "Lamentations": "lam",
    "Ezekiel": "eze",
    "Daniel": "dan",
    "Hosea": "hos",
    "Joel": "joe",
    "Amos": "amo",
    "Obadiah": "oba",
    "Jonah": "jon",
    "Micah": "mic",
    "Nahum": "nah",
    "Habakkuk": "hab",
    "Zephaniah": "zep",
    "Haggai": "hag",
    "Zechariah": "zac",
    "Malachi": "mal",
    "1 Esdras": "es1",
    "2 Esdras": "es2",
    "Tobias": "tob",
    "Judith": "jdt",
    "Additions to Esther": "aes",
    "Wisdom": "wis",
    "Baruch": "bar",
    "Epistle of Jeremiah": "epj",
    "Susanna": "sus",
    "Bel and the Dragon": "bel",
    "Prayer of Manasseh": "man",
    "1 Macabees": "ma1",
    "2 Macabees": "ma2",
    "3 Macabees": "ma3",
    "4 Macabees": "ma4",
    "Sirach": "sir",
    "Prayer of Azariah": "aza",
    "Laodiceans": "lao",
    "Joshua B": "jsb",
    "Joshua A": "jsa",
    "Judges B": "jdb",
    "Judges A": "jda",
    "Tobit BA": "toa",
    "Tobit S": "tos",
    "Psalms of Solomon": "pss",
    "Bel and the Dragon Th": "bet",
    "Daniel Th": "dat",
    "Susanna Th": "sut",
    "Odes": "ode",
    "Matthew": "mat",
    "Mark": "mar",
    "Luke": "luk",
    "John": "joh",
    "Acts": "act",
    "Romans": "rom",
    "1 Corinthians": "co1",
    "2 Corinthians": "co2",
    "Galatians": "gal",
    "Ephesians": "eph",
    "Philippians": "phi",
    "Colossians": "col",
    "1 Thessalonians": "th1",
    "2 Thessalonians": "th2",
    "1 Timothy": "ti1",
    "2 Timothy": "ti2",
    "Titus": "tit",
    "Philemon": "plm",
    "Hebrews": "heb",
    "James": "jam",
    "1 Peter": "pe1",
    "2 Peter": "pe2",
    "1 John": "jo1",
    "2 John": "jo2",
    "3 John": "jo3",
    "Jude": "jde",
    "Revelation": "rev"
}

class KJVParser:
    def __init__(self, bookdir):
        self.bookdir = bookdir
        self.currentbook = None
        self.bookcontent = {}

    def parseBook(self, bookabbr):
        filepath = self.bookdir+'/'+'kjvdat.txt'
        self.currentbook = bookabbr
        self.bookcontent = defaultdict(lambda : {})
        try:
            bookname = abbr.getBookName(bookabbr)
        except KeyError:
            raise NoBibleBookException(bookabbr)
        datbookname = bknameref[bookname]

        bibdat = open(filepath, 'rb')
        for line in bibdat:
            bkname, chap, verse, scripture = line.split('|')
            if bkname.lower()==datbookname.lower():
                chap = int(chap)
                verse = int(verse)
                scripture = scripture.strip()
                self.bookcontent[chap][verse] = scripture[:-1] if re.search('~$', scripture) else scripture
        bibdat.close()
        self.bookcontent = dict(self.bookcontent)

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
            #sys.stderr.write('No verse: '+bookabbr+' '+str(chap)+':'+str(verse)+'\n')
            #scripture = ''
            raise InvalidBibleLocationException(bookabbr, chap, verse)
        return scripture

    def retrieveVersesIterator(self, bookabbr, startChap, startVerse, endChap, endVerse):
        # validation
        if startChap > endChap or (startChap==endChap and startVerse>endVerse):
            raise BibleException('Wrong chapter sequence: '+str(startChap)+'>'+str(endChap))
        if bookabbr != self.currentbook:
            self.parseBook(bookabbr)
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
                yield (bookabbr, chap, verse, self.retrieveVerse(bookabbr, chap, verse))

    def retrieveVerses(self, bookabbr, startChap, startVerse, endChap, endVerse):
        versesIterator = self.retrieveVersesIterator(bookabbr, startChap, startVerse, endChap, endVerse)
        return ' '.join([verseTuple[3] for verseTuple in versesIterator])