__author__ = 'hok1'

from gensim.models import word2vec
import nltk
import numpy as np
import re


class DocVectorizer:
    def __init__(self, modelfilename, binary=True, toRemoveDigits=True, toLower=True, toRemoveStopWords=True,
                 toStemWords=False):
        self.loadmodel(modelfilename, binary=binary)
        self.toRemoveDigits = toRemoveDigits
        self.toLower = toLower
        self.toRemoveStopWords = toRemoveStopWords
        self.toStemWords = toStemWords

        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()
        if (self.toStemWords):
            self.stemmer = nltk.stem.PorterStemmer()

    def loadmodel(self, modelfilename, binary=True):
        self.wmodel = word2vec.Word2Vec.load_word2vec_format(modelfilename, binary=binary)

    def vectorizeDoc(self, docstr):
        norm_docstr = re.sub('\\W', ' ', docstr)
        if (self.toRemoveDigits):
            norm_docstr = re.sub('\\d', ' ', norm_docstr)
        norm_docstr = re.sub('\\s+', ' ', norm_docstr)
        if (self.toRemoveStopWords):
            pass
        if (self.toLower):
            norm_docstr = norm_docstr.lower()

