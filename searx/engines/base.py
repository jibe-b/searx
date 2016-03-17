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

import re

categories = ['science']

base_url = 'https://api.base-search.net/cgi-bin/BaseHttpSearchInterface.fcgi?func=PerformSearch&{query}&boost=oa&hits={hits}&offset={offset}'


# engine dependent config
paging = True
number_of_results = 10


def request(query, params):

    #enable shortcut for advanced search
    dico={
            'format' : 'dcformat',
            'author' : 'dccreator',
            'collection' : 'dccollection',
            'hdate' : 'dchdate',
            'contributor' : 'dccontributor',
            'coverage' : 'dccoverage',
            'date' : 'dcdate',
            'abstract' : 'dcdescription',
            'urls' : 'dcidentifier',
            'language' : 'dclanguage',
            'publisher' : 'dcpublisher',
            'relation' : 'dcrelation',
            'rights' : 'dcrights',
            'source' : 'dcsource',
            'subject' : 'dcsubject',
            'title' : 'dctitle',
            'type' : 'dcdctype'  
    }

    for key in dico.keys():
        query = re.sub(str(key),  str(dico[key]), query)



    #regular search
    offset = (params['pageno'] - 1  ) * number_of_results

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
	
	date = datetime.now() #needed in case no dcdate is available for an item
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
        for date_format in ['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d', '%Y-%m', '%Y']:
            try:
        	publishedDate = datetime.strptime(date, date_format)
        	break
    	    except:
                try:
                    publishedDate = datetime.strptime(harvestDate,  date_format )
                    content = "Publisehd: " + str(date) + " - " + content
                except:
                    pass


	if publishedDate != None:
	    res_dict = {'url': url,
                        'title': title,
			'publishedDate': publishedDate,
			'content': content}
        else:
            res_dict = {'url': url,
                        'title': title,
                        'content': content}

        results.append(res_dict)

    return results
