__author__ = 'hok1'

from gensim.models import word2vec
from gensim import corpora
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
import re
import numpy as np

class DocVectorizer:
    def __init__(self, modelfilename=None, binary=True, toRemoveDigits=True, toLower=True, toRemoveStopWords=True):
        if modelfilename != None:
            self.loadmodel(modelfilename, binary=binary)
        self.toRemoveDigits = toRemoveDigits
        self.toLower = toLower
        self.toRemoveStopWords = toRemoveStopWords
        self.tokenizer = TreebankWordTokenizer()

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
            tokenizedDoc = filter(lambda s: not (s.lower() in stopwords.words()), tokenizedDoc)
        return tokenizedDoc

    def retrieveWord2VecDocVectors(self, docstr):
        tokens = self.tokenizeDoc(docstr)
        vectors = map(lambda token: self.wmodel[token] if (token in self.wmodel) else None, tokens)
        filteredPairs = filter(lambda pair: pair[1]!=None, zip(tokens, vectors))
        tokens = map(lambda pair: pair[0], filteredPairs)
        vectors = np.array(map(lambda pair: pair[1], filteredPairs))
        return tokens, vectors

    def retrieveGensimCorpora(self, docs, stemfunc=lambda s: s):
        texts = map(self.tokenizeDoc, docs)
        texts = map(lambda text: map(stemfunc, text), texts)
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        return dictionary, corpus