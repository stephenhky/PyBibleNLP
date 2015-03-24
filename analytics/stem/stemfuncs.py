__author__ = 'hok1'

from Bible.BibleExceptions import BibleException
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

class NoStemmerException(BibleException):
    def __init__(self):
        self._message = 'No such stemmer!'

def getstemfunc(stemmerkey):
    if stemmerkey=='':
        stemfunc = lambda s: s
    elif stemmerkey=='porter':
        porterStemmer = PorterStemmer()
        stemfunc = lambda s: porterStemmer.stem(s)
    elif stemmerkey=='lancaster':
        lancasterStemmer = LancasterStemmer()
        stemfunc = lambda s: lancasterStemmer.stem(s)
    elif stemmerkey=='wordnetLemmatizer':
        lemmatizer = WordNetLemmatizer()
        stemfunc = lambda s: str(min(lemmatizer.lemmatize(s, 'v'), lemmatizer.lemmatize(s, 'n'),
                                     key=lambda st: len(st))
        )
    else:
        raise NoStemmerException()
    return stemfunc