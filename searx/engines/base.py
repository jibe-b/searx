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
from searx.utils import searx_useragent
from cgi import escape

from datetime import datetime
from string import Formatter

categories = ['science']

base_url = 'https://api.base-search.net/cgi-bin/BaseHttpSearchInterface.fcgi?func=PerformSearch&{query}&hits={hits}&offset={offset}'


# engine dependent config
paging = True
number_of_results = 10


def request(query, params):

    offset = (params['pageno'] - 1  ) * number_of_results
    print (params['pageno'] -1)* number_of_results 

    string_args = dict(query=urlencode({'query': query}),
                       offset=offset,
                       hits=number_of_results)

    format_strings = list(Formatter().parse(base_url))

    search_url = base_url

    params['url'] = search_url.format(**string_args)

    params['headers']['User-Agent'] = searx_useragent()
    return params


def response(resp):
    results = []

    search_results = etree.XML(resp.content)

    for entry in search_results.xpath('./result/doc'):
        content = "No description available"

        for item in entry:
            if item.attrib["name"] == "dchdate":
                harvestDate = item.text

            if item.attrib["name"] == "dcdate":
                date = item.text

            if item.attrib["name"] == "dctitle":
                title = item.text        

            elif item.attrib["name"] == "dclink":
                url = item.text

            elif item.attrib["name"] == "dcdescription":
                content = escape(item.text[:300]) + "..."

        #tmp: dates returned by the BASE API are not in iso format
        #so the three main date formats are tried one after the other
        try: 
            publishedDate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ' )
        except:
            try:
                publishedDate = datetime.strptime(date, '%Y' ) 
            except:
                try:
                    publishedDate = datetime.strptime(date, '%Y-%m-%d' )
                except:
                    try:
                        publishedDate = datetime.strptime(harvestDate,  '%Y-%m-%dT%H:%M:%SZ' )
                    except:
                        publishedDate = datetime.now()
                    finally:
                        content = "Published: " + str(date) + " - " + content


        results.append({'url': url,
                        'title': title,
                        'publishedDate': publishedDate,
                        'content': content})

    return results
