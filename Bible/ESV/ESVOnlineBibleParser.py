__author__ = 'hok1'

import Bible.BookAbbrDict as abbr
import urllib
import urllib2

baseurl = 'http://www.esvapi.org/v2/rest/'

class ESVOnlineParser:
    def __init__(self, key):
        self.key = key

    def query(self, bookabbr, chapidx):
        bookname = abbr.getBookName(bookabbr)
        query_args = {'key': self.key, 'passage': bookname+' '+str(chapidx), 'output-format': 'crossway-xml-1.0'}
        query_url = baseurl+'passageQuery?'+urllib.urlencode(query_args)
        return urllib2.urlopen(query_url)

    def save_url(self, path, response):
        fout = open(path, 'wb')
        fout.writelines(response.readlines())
        fout.close()
