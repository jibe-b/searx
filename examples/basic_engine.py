
categories = ['science'] # optional

def request(query, params):
    '''pre-request callback
    params<dict>:
      method  : POST/GET
      headers : {}
      data    : {} # if method == POST
      url     : ''
      category: 'search category'
      pageno  : 1 # number of the requested page
    '''

    params['url'] = 'https://api.base-search.net/cgi-bin/BaseHttpSearchInterface.fcgi?func=PerformSearch&target=%s' % query

    return params


def response(resp):
    '''post-response callback
    resp: requests response object
    '''
    return [{'url': '', 'title': '', 'content': ''}]

