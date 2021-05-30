import unittest
from unittest.mock import MagicMock

import responses

from domain.commerce_system.user import Subscribed, User


class TestNotifications(unittest.TestCase):

    def register_and_login(self, username, password) -> Subscribed:
        user = User()
        sub = user.register(username, password=password)
        user.login(sub)
        return user

    def test_message_added_to_pending(self):
        u = self.register_and_login("A", "a")
        n = u.user_state.notifications
        # n.send_message = MagicMock(return_value=None)
        n.clients = {}
        u.send_message("Hel")
        self.assertEqual(len(n.pending_messages), 1)

    def test_message_sent_to_user(self):
        u = self.register_and_login("A", "a")
        n = u.user_state.notifications
        n.send_message = MagicMock(return_value=None)
        n.add_client(u.id, 1)
        u.send_message("Hel")
        self.assertEqual(len(n.pending_messages), 0)

    def test_send_pending_messages_to_user(self):
        u = self.register_and_login("A", "a")
        n = u.user_state.notifications
        n.send_message = MagicMock(return_value=None)
        n.clients = {}
        u.send_message("Hel")
        n.add_client(u.id, 1)
        self.assertEqual(len(n.pending_messages), 0)

    def test_disconnect_user_right_value(self):
        u = self.register_and_login("A", "a")
        n = u.user_state.notifications
        n.send_message = MagicMock(return_value=None)
        n.add_client(u.id, 2)
        n.disconnect(2)
        self.assertEqual(len(n.clients.keys()), 0)

    def test_disconnect_user_wrong_value(self):
        u = self.register_and_login("A", "a")
        n = u.user_state.notifications
        n.send_message = MagicMock(return_value=None)
        n.add_client(u.id, 2)
        n.disconnect(1)
        self.assertEqual(len(n.clients.keys()), 1)


if __name__ == '__main__':
    unittest.main()
