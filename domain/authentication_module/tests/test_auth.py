import unittest

from domain.authentication_module.authenticator import Authenticator


class TestAuthenticator(unittest.TestCase):
    def test_fail_register(self):
        auth = Authenticator()
        self.assertRaises(AssertionError, auth.register_new_user, "aviv", "123")

    def test_success_register(self):
        auth = Authenticator()
        auth.register_new_user("aviv", "123456")

    def test_fail_login(self):
        auth = Authenticator()
        username = "aviv"
        password = "123456"
        auth.register_new_user(username, password)
        self.assertRaises(AssertionError, auth.login, username, "123")

    def test_success_login(self):
        auth = Authenticator()
        username = "aviv"
        password = "123456"
        auth.register_new_user(username, password)
        auth.login(username, password)
