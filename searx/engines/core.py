#!/usr/bin/env python

"""
 CORE (Scholar publications)

 @website     https://core.ac.uk
 @provide-api yes with authorization (https://core.ac.uk/api-v2/)

 @using-api   yes
 @results     XML
 @stable      ?
 @parse       url, title, publishedDate, content
 More info on api: https://core.ac.uk/docs/
 Register API key: https://core.ac.uk/api-keys/register
"""

import json
from datetime import datetime
import re
from searx.url_utils import urlencode
from searx import settings

categories = ['science']

base_url = 'https://core.ac.uk:443/api-v2/articles/search/data?metadata=true&fulltext=false'\
           + '&citations=false&similar=false&duplicate=false&urls=true&faithfulMetadata=false'\
           + '&page={offset}&pageSize={number_of_results}&apiKey={api_key}'

# engine dependent config
paging = True
number_of_results = 10
api_key = settings['api_keys']['core_api']


def request(query, params):
    offset = (params['pageno'] - 1)

    string_args = dict(query=urlencode({'query': query}),
                       api_key=api_key,
                       offset=offset,
                       number_of_results=number_of_results)

    params['url'] = base_url.format(**string_args)
    return params


def response(resp):
    results = []

    search_results = json.loads(resp.text)

    date_formats = ['%Y-%m-%d', '%Y:%m:%d']

    publishedDate = None
    for entry in search_results['data']:
        for date_format in date_formats:
            try:
                publishedDate = datetime.strptime(entry['datePublished'], '%Y-%m-%d')
            except:
                pass

        try:
            doi = entry['doi']

        except:
            doi = ''

        title = entry['title']

        url = entry['downloadUrl']

        if doi is not '':
            content = 'DOI: ' + doi + ' ' + entry['description'][:300]
        else:
            content = entry['description'][:300]

        if len(content) > 300:
            content += '...'

        res_dict = {'url': url,
                    'title': title,
                    'content': content}

        if publishedDate is not None:
            res_dict['publishedDate'] = publishedDate

        results.append(res_dict)

    return results
