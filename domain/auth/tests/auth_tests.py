import unittest
from unittest.mock import MagicMock

from domain.auth.authenticator import Authenticator


class TestAuthenticator(unittest.TestCase):

    def test_generate_token1(self):
        auth = Authenticator()
        new_token = auth.generate_token()
        assert len(new_token) == 8

    def test_generate_token2(self):
        auth = Authenticator()
        new_token = auth.generate_token()
        assert new_token not in auth.tokens_ids

    def test_add_new_user_token1(self):
        auth = Authenticator()
        user_id = 2
        auth.add_new_user_token(user_id)
        assert len(auth.tokens_ids) == 1

    def test_add_new_user_token2(self):
        auth = Authenticator()
        user_id = 2
        dummy_token = '12345678'
        auth.generate_token = MagicMock(return_value=dummy_token)
        auth.add_new_user_token(user_id)
        assert auth.tokens_ids[dummy_token] == user_id

    def test_remove_token1(self):
        auth = Authenticator()
        user_id = 2
        dummy_token = '12345678'
        auth.generate_token = MagicMock(return_value=dummy_token)
        auth.add_new_user_token(user_id)
        auth.remove_token(dummy_token)
        assert len(auth.tokens_ids) == 0

    def test_remove_token2(self):
        auth = Authenticator()
        user_id = 2
        dummy_token = '12345678'
        auth.generate_token = MagicMock(return_value=dummy_token)
        auth.add_new_user_token(user_id)
        ret_val = auth.remove_token(dummy_token)
        assert ret_val == user_id

    def test_remove_token3(self):
        auth = Authenticator()
        user_id = 2
        dummy_token = '12345678'
        auth.generate_token = MagicMock(return_value=dummy_token)
        auth.add_new_user_token(user_id)
        other_token = '12345677'
        ret_val = auth.remove_token(other_token)
        assert ret_val == -1




