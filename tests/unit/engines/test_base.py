# -*- coding: utf-8 -*-
import mock
from searx.engines import base
from searx.testing import SearxTestCase

class TestBaseEngine(SearxTestCase):

    def test_request(self):
        query = 'test_query'
        api_key = 'XXXXXX-XXXXXXXXXX'
        dicto = defaultdict(dict)
        dicto['api_key'] = api_key
        params = base.request(query, dicto)

        self.assertIn('url', params)
        self.assertIn(query, params['url'])
        self.assertIn('base-search.net', params['url'])

        self.assertIn('api_key', params)

    def test_response(self):
        self.assertRaises(AttributeError, base.response, None)
	# and other exapmles of error responses
        
        xml = '''<?xml version='1.0' encoding='UTF-8'?>
        <queryresult success='false' error='false' />
        '''
#example of tests

        # test failure
        response = mock.Mock(content=xml)
        self.assertEqual(base.response(response), [])

        xml = """<?xml version='1.0' encoding='UTF-8'?>                    [...]"""

        # test integral
        response = mock.Mock(content=xml)
        results = wolframalpha_api.response(response)
        self.assertEqual(type(results), list)
        self.assertEqual(len(results), 2)
        self.assertIn('log(x)+c', results[0]['answer'])
        self.assertIn('∫1/xx - Wolfram|Alpha'.decode('utf-8'), results[1]['title'])
        self.assertEquals('http://www.wolframalpha.com/input/?i=%E2%88%AB1%2Fx%EF%9D%8Cx', results[1]['url'])

        xml = """<?xml version='1.0' encoding='UTF-8'?> """
