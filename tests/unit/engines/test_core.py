# -*- coding: utf-8 -*-
from collections import defaultdict
import mock
from searx.engines import core
from searx.testing import SearxTestCase


class TestCoreEngine(SearxTestCase):

    def test_request(self):
        query = 'test_query'
        dicto = defaultdict(dict)
        dicto['pageno'] = 1
        params = core.request(query, dicto)
        self.assertIn('url', params)
        self.assertIn('core.ac.uk', params['url'])

    def test_response(self):
        self.assertRaises(AttributeError, core.response, None)
        self.assertRaises(AttributeError, core.response, '')
        self.assertRaises(AttributeError, core.response, [])
        self.assertRaises(AttributeError, core.response, '[]')

        response = mock.Mock(text='{"data": []}')
        self.assertEqual(core.response(response), [])

        json_mock = '''{
  "status": "OK",
  "totalHits": 1,
  "data": [
    {
      "id": "87654321",
      "authors": [
        "Alpha, Bravo"
      ],
      "contributors": [],
      "datePublished": "2000-01-01",
      "description": "Some scientific content.",
      "identifiers": [
        "10.1000/xyz123"
      ],
      "language": {
        "code": "en",
        "id": 9,
        "name": "English"
      },
      "relations": [],
      "subjects": [
        "text"
      ],
      "title": "Scientific discovery",
      "topics": [
        "Science"
      ],
      "types": [],
      "year": 2000,
      "fulltextUrls": [
        "https://core.ac.uk/download/pdf/87654321.pdf"
      ],
      "fulltextIdentifier": "https://core.ac.uk/download/pdf/87654321.pdf",
      "doi": "10.1000/xyz123",
      "oai": "",
      "downloadUrl": "http://arxiv.org/abs/0000-0000"
    }]}'''

        response = mock.Mock(text=json_mock)
        results = core.response(response)
        self.assertEqual(type(results), list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['content'], 'DOI: 10.1000/xyz123 Some scientific content.')
