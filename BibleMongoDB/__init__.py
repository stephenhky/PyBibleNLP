__author__ = 'hok1'

# remember to run " mongod --config /usr/local/etc/mongod.conf " before using MongoDB package

from pymongo import MongoClient

dbname = 'PyBibleNLP'
client = MongoClient()
bibledb = client[dbname]