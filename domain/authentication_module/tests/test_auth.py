import unittest

from domain.authentication_module.authenticator import Authenticator
from data_access_layer.init_tables import engine

class TestAuthenticator(unittest.TestCase):
    def test_fail_register(self):
        auth = Authenticator()
        self.assertRaises(AssertionError, auth.register_new_user, "aviv1234", "123")

    def test_success_register(self):
        auth = Authenticator()
        auth.register_new_user("aviv12", "123456")

    def test_fail_login(self):
        auth = Authenticator()
        username = "aviv1111111111"
        password = "123456"
        auth.register_new_user(username, password)
        self.assertRaises(AssertionError, auth.login, username, "123")

    def test_success_login(self):
        auth = Authenticator()
        username = "aviv245"
        password = "123456"
        auth.register_new_user(username, password)
        auth.login(username, password)
