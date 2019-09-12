from unittest import TestCase, mock
from aiohttp_oauth_client import OAuth1Client


class OAuth1ClientTest(TestCase):
    def test_no_client_id(self):
        self.assertRaises(ValueError, lambda: OAuth1Client(None))
