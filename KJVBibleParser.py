__author__ = 'hok1'

import BookAbbrDict as abbr
import re

ChapIndicatorRE = "CHAPTER [1-9][0-9]|CHAPTER [0-9]|PSALM [1-9][1-9][0-9]|PSALM [1-9][0-9]|PSALM [0-9]"

class KJVParser:
    def __init__(self, bookdir):
        self.bookdir = bookdir
        self.currentbook = None
        self.bookcontent = {}

    def parseBook(self, bookabbr):
        basefilename = abbr.getBookName(bookabbr)+'.txt'
        filepath = self.bookdir + '/' + basefilename
        self.currentbook = bookabbr
        self.bookcontent = {}

        fin = open(filepath, 'rb')
        fin.readline()
        fin.readline()
        chapIdx = 0
        verseIdx = 0
        for line in fin.readline():
            line = line.strip()
            re.match(ChapIndicatorRE, line)
            firstSpacePos = line.find(' ')

