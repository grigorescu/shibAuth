"""These tests submits 4 POST requests to an application behind Shib."""

__author__ = 'vladg'

import unittest
import requests
from shibAuth.auth import ShibAuth
import shibAuth.config

class TestShibFunctions(unittest.TestCase):
    def setUp(self):
        self.session = requests.session(
            auth=ShibAuth(shibAuth.config.username,
                          shibAuth.config.password),
            verify=shibAuth.config.verify)

    def test_init(self):
        self.assertTrue(self.session)

    def test_query_one(self):
        result = self.session.post(shibAuth.config.application_url,
                                   data=shibAuth.config.test1,
                                   allow_redirects=True)
        self.assertTrue(shibAuth.config.result1 in result.content)

    def test_query_two(self):
        result = self.session.post(shibAuth.config.application_url,
                                   data=shibAuth.config.test2,
                                   allow_redirects=True)
        self.assertTrue(shibAuth.config.result2 in result.content)

    def test_query_three(self):
        result = self.session.post(shibAuth.config.application_url,
                                   data=shibAuth.config.test1,
                                   allow_redirects=True)
        self.assertFalse(shibAuth.config.result2 in result.content)

    def test_query_four(self):
        result = self.session.post(shibAuth.config.application_url,
                                   data=shibAuth.config.test2,
                                   allow_redirects=True)
        self.assertFalse(shibAuth.config.result1 in result.content)

if __name__ == '__main__':
    unittest.main()
