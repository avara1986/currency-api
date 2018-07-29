import json
import unittest

import requests_mock

from currency_providers.requests import Request


class SimpleTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_provider(self):
        provider_to_get = "mock"


class RequestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://localhost:8000/"

        cls.request = Request(base_url=cls.base_url)

    @requests_mock.mock()
    def test_url(self, mock_requests):
        prefix_url = "my-endpoint/"
        response_json = {"a": "b"}
        mock_requests.get(self.base_url + prefix_url, text=json.dumps(response_json))
        response, content = self.request.request(url=prefix_url, method="get", data={})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(content, response_json)

    def test_fail_url(self):
        prefix_url = "my-endpoint-that-not-exist/"
        response, content = self.request.request(url=prefix_url, method="get", data={})
        self.assertEquals(response, False)
        self.assertIn("HTTPConnectionPool(host=", content)
