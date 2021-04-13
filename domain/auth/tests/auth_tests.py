import unittest
from unittest.mock import MagicMock

from domain.auth.authenticator import Authenticator


class TestAuthenticator(unittest.TestCase):

    def test_generate_token1(self):
        auth = Authenticator()
        user_id = 11
        new_token = auth.generate_token(id)
        assert len(new_token) == 8

    def test_generate_token2(self):
        auth = Authenticator()
        user_id = 11
        new_token = auth.generate_token(id)
        assert new_token in auth.tokens_ids

    def test_generate_token3(self):
        auth = Authenticator()
        user_id = 11
        new_token = auth.generate_token(id)
        assert user_id == auth.tokens_ids[new_token]