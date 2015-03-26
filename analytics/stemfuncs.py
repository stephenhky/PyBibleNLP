__author__ = 'hok1'

from Bible.BibleExceptions import BibleException

class NoStemmerException(BibleException):
    def __init__(self):
        self._message = 'No such stemmer!'

def getstemfunc(stemmerkey):
    if stemmerkey=='':
        stemfunc = lambda s: s
    elif stemmerkey=='porter':
        from nltk.stem.porter import PorterStemmer
        porterStemmer = PorterStemmer()
        stemfunc = lambda s: porterStemmer.stem(s)
    elif stemmerkey=='lancaster':
        from nltk.stem.lancaster import LancasterStemmer
        lancasterStemmer = LancasterStemmer()
        stemfunc = lambda s: lancasterStemmer.stem(s)
    elif stemmerkey=='wordnetLemmatizer':
        from nltk.stem.wordnet import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        stemfunc = lambda s: str(min(lemmatizer.lemmatize(s, 'v'), lemmatizer.lemmatize(s, 'n'),
                                     key=lambda st: len(st))
        )
    else:
        raise NoStemmerException()
    return stemfunc