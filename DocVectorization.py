__author__ = 'hok1'

from gensim.models import word2vec
import nltk
import re

class DocVectorizer:
    def __init__(self, modelfilename, binary=True, toRemoveDigits=True, toLower=True, toRemoveStopWords=True):
        self.loadmodel(modelfilename, binary=binary)
        self.toRemoveDigits = toRemoveDigits
        self.toLower = toLower
        self.toRemoveStopWords = toRemoveStopWords
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def loadmodel(self, modelfilename, binary=True):
        self.wmodel = word2vec.Word2Vec.load_word2vec_format(modelfilename, binary=binary)

    def unloadmodel(self):
        self.wmodel = None

    def tokenizeDoc(self, docstr):
        tokenizedDoc = self.tokenizer.tokenize(docstr)
        tokenizedDoc = filter(lambda t: re.match('\\W', t)==None, tokenizedDoc)
        tokenizedDoc = map(lambda s: re.sub('\\W', '', s), tokenizedDoc)
        if self.toRemoveDigits:
            tokenizedDoc = filter(lambda token: re.match('\\d', token)==None, tokenizedDoc)
        if self.toLower:
            tokenizedDoc = map(lambda s: s.lower(), tokenizedDoc)
        if self.toRemoveStopWords:
            tokenizedDoc = filter(lambda s: not (s.lower() in nltk.corpus.stopwords.words()), tokenizedDoc)
        return tokenizedDoc

    def retrieveDocVectors(self, docstr):
        tokens = self.tokenizeDoc(docstr)
        vectors = map(lambda token: self.wmodel[token] if (token in self.wmodel) else None, tokens)
        return tokens, vectors
