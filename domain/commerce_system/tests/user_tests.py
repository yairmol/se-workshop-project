import unittest
from unittest.mock import MagicMock
from domain.auth.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.user import User, Subscribed


class TestCommerceSystemFacade(unittest.TestCase):

    def test_add_active_user1(self):

        facade = CommerceSystemFacade()
        facade.enter()
        assert len(facade.active_users) == 1

    def test_user_register1(self):
        user = User()
        try:
            sub = user.register("aviv", "123456")
            print(type(sub))
            assert isinstance(sub, Subscribed)
        except Exception as e:
            assert False

    def test_user_register2(self):
        user = User()
        user.user_state = Subscribed("aviv", "123456")
        try:
            sub = user.register("aviv", "123456")
            assert False
        except Exception as e:
            assert True