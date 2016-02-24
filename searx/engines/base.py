#!/usr/bin/env python

"""
 BASE (Scholar publications)

 @website     https://base-search.net
 @provide-api yes with authorization (https://api.base-search.net/)

 @using-api   yes
 @results     XML
 @stable      ?
 @parse       ?
 More info on api advanced search : http://base-search.net/about/download/base_interface.pdf 
"""

from lxml import etree
from urllib import urlencode
from json import loads
from searx.utils import searx_useragent
from cgi import escape

from datetime import datetime

categories = ['science']

url = 'https://api.base-search.net/cgi-bin/BaseHttpSearchInterface.fcgi?func=PerformSearch&{query}'

def validate_date(d):
    try:
        datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S%z')
        return True
    except ValueError:
        return False

def request(query, params):
    params['url'] = url.format(query=urlencode({'query': query}))
    params['headers']['User-Agent'] = searx_useragent()
    return params


def response(resp):
    results = []

    search_results = etree.XML(resp.content)

    for entry in search_results.xpath('./result/doc'):
        content = "No description available"
        publishedDate = datetime.now()

        for item in entry:
            if item.attrib["name"] == "dchdate":
                date = item.text 

            if item.attrib["name"] == "dcdate":
                harvestDate = item.text

            if item.attrib["name"] == "dctitle":
                title = item.text        

            elif item.attrib["name"] == "dclink":
                url = item.text

            elif item.attrib["name"] == "dcdescription":
                content = escape(item.text[:500])

        #tmp: dates returned by the BASE API are not in iso format
        if validate_date(date) == False:
            content = str(date) + " - " + content
            publishedDate = harvestDate

        if validate_date(harvestDate) == False:
            publishedDate = datetime.now()  

	#tmp
	publishedDate = datetime.now()

        results.append({'url': url,
                        'title': title,
                        'publishedDate': publishedDate,
                        'content': content})

    return results
