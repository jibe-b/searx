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

from urllib import urlencode
from json import loads
from searx.utils import searx_useragent
from cgi import escape

categories = ['science']

url = 'https://api.base-search.net/cgi-bin/BaseHttpSearchInterface.fcgi?func=PerformSearch&query={query}'

def request(query, params):
    params['url'] = url.format(text=urlencode({'query': query}))
    params['headers']['User-Agent'] = searx_useragent()
    return params


def response(resp):
    results = []

    search_results = etree.XML(resp.content)

    for entry in search_results.xpath('./result')[0]:
        url = "none"
        description = "none"
        for i, item in enumerate(entry):
            att = item.attrib
            if att["name"] == "dclink":
                url = item.text
            elif att["name"] == "dctitle":
                title = item.text    
            elif att["name"] == "dcdate":
                date = item.text
            elif att["name"] == "dcdescription":
                description = escape(item.text[:500])

        results.append({'url': url,
                        'title': title,
                        'publishedDate': publishedDate,
                        'content': description})
