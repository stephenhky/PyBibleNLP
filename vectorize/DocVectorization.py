__author__ = 'hok1'

from gensim import corpora
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
import re

class DocVectorizer:
    def __init__(self, toRemoveDigits=True, toLower=True, toRemoveStopWords=True):
        self.toRemoveDigits = toRemoveDigits
        self.toLower = toLower
        self.toRemoveStopWords = toRemoveStopWords
        self.tokenizer = TreebankWordTokenizer()

    def tokenizeDoc(self, docstr):
        tokenizedDoc = self.tokenizer.tokenize(docstr)
        tokenizedDoc = filter(lambda t: re.match('\\W', t)==None, tokenizedDoc)
        tokenizedDoc = map(lambda s: re.sub('\\W', '', s), tokenizedDoc)
        if self.toRemoveDigits:
            tokenizedDoc = filter(lambda token: re.match('\\d', token)==None, tokenizedDoc)
        if self.toLower:
            tokenizedDoc = map(lambda s: s.lower(), tokenizedDoc)
        if self.toRemoveStopWords:
            tokenizedDoc = filter(lambda s: not (s.lower() in stopwords.words()), tokenizedDoc)
        return tokenizedDoc

    def retrieveGensimCorpora(self, docs, stemfunc=lambda s: s):
        texts = map(self.tokenizeDoc, docs)
        texts = map(lambda text: map(stemfunc, text), texts)
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        return dictionary, corpus