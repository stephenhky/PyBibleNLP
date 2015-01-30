__author__ = 'hok1'

class BibleException(Exception):
    def __init__(self, msg):
        self.message = msg

class NoBibleBookException(BibleException):
    def __init__(self, bookabbr):
        self.message = 'No such book ('+bookabbr+') exists.'

class InvalidBibleLocationException(BibleException):
    def __init__(self, bookabbr, chap, verse):
        self.message = 'No such location '+bookabbr+' '+str(chap)+':'+str(verse)

class InvalidBibleChapterException(BibleException):
    def __init__(self, bookabbr, chap):
        self.message = 'The book '+bookabbr+' does not have chapter '+str(chap)