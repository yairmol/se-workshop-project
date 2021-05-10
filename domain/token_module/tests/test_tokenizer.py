import unittest
from unittest.mock import MagicMock

from domain.token_module.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):

    def test_generate_token1(self):
        tokenizer = Tokenizer()
        new_token = tokenizer.generate_token()
        assert len(new_token) == 8

    def test_generate_token2(self):
        tokenizer = Tokenizer()
        new_token = tokenizer.generate_token()
        assert new_token not in tokenizer.tokens_ids

    def test_add_new_user_token1(self):
        tokenizer = Tokenizer()
        user_id = 2
        tokenizer.add_new_user_token(user_id)
        assert len(tokenizer.tokens_ids) == 1

    def test_add_new_user_token2(self):
        tokenizer = Tokenizer()
        user_id = 2
        dummy_token = '12345678'
        tokenizer.generate_token = MagicMock(return_value=dummy_token)
        tokenizer.add_new_user_token(user_id)
        assert tokenizer.tokens_ids[dummy_token] == user_id

    def test_remove_token1(self):
        tokenizer = Tokenizer()
        user_id = 2
        dummy_token = '12345678'
        tokenizer.generate_token = MagicMock(return_value=dummy_token)
        tokenizer.add_new_user_token(user_id)
        tokenizer.remove_token(dummy_token)
        assert len(tokenizer.tokens_ids) == 0

    def test_remove_token2(self):
        tokenizer = Tokenizer()
        user_id = 2
        dummy_token = '12345678'
        tokenizer.generate_token = MagicMock(return_value=dummy_token)
        tokenizer.add_new_user_token(user_id)
        ret_val = tokenizer.remove_token(dummy_token)
        assert ret_val == user_id

    def test_remove_token3(self):
        tokenizer = Tokenizer()
        user_id = 2
        dummy_token = '12345678'
        tokenizer.generate_token = MagicMock(return_value=dummy_token)
        tokenizer.add_new_user_token(user_id)
        other_token = '12345677'
        ret_val = tokenizer.remove_token(other_token)
        assert ret_val == -1

    def test_is_token_expired1(self):
        tokenizer = Tokenizer()
        user_id = 2
        dummy_token = '12345678'
        tokenizer.generate_token = MagicMock(return_value=dummy_token)
        tokenizer.add_new_user_token(user_id)
        assert not tokenizer.is_token_expired(dummy_token)

    def test_is_token_expired2(self):
        tokenizer = Tokenizer()
        user_id = 2
        dummy_token = '12345678'
        tokenizer.generate_token = MagicMock(return_value=dummy_token)
        tokenizer.add_new_user_token(user_id)
        other_token = '12345677'
        assert tokenizer.is_token_expired(other_token)
