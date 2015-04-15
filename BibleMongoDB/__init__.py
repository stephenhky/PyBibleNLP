__author__ = 'hok1'

from pymongo import MongoClient

dbname = 'PyBibleNLP'
client = MongoClient()
bibledb = client[dbname]