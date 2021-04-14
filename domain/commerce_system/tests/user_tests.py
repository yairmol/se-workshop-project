import unittest
from unittest.mock import MagicMock
from domain.auth.authenticator import Authenticator
from domain.commerce_system.user_managment import UserManagement


class TestUserManagement(unittest.TestCase):

    def test_add_active_user1(self):
        auth = Authenticator()
        dummy_token = '12345678'
        auth.generate_token = MagicMock(return_value=dummy_token)
        user_management = UserManagement(auth)
        assert user_management.add_active_user() == '12345678'

    def test_add_active_user2(self):
        auth = Authenticator()
        dummy_token = '12345678'
        auth.generate_token = MagicMock(return_value= dummy_token)
        user_management = UserManagement(auth)
        user_management.add_active_user()
        assert len(user_management.active_users) == 1

    def test_remove_active_user1(self):
        auth = Authenticator()
        dummy_token = '12345678'
        auth.generate_token = MagicMock(return_value=dummy_token)
        user_management = UserManagement(auth)
        user_management.add_active_user()
        user_management.remove_active_user(dummy_token)
        assert len(user_management.active_users) == 0

    def test_remove_active_user2(self):
        auth = Authenticator()
        dummy_token = '12345678'
        auth.generate_token = MagicMock(return_value=dummy_token)
        user_management = UserManagement(auth)
        user_management.add_active_user()
        other_token = '12345677'
        user_management.remove_active_user(other_token)
        assert len(user_management.active_users) == 1
