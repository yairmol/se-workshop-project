import unittest
from unittest.mock import MagicMock

from domain.notifications.notifications import Notifications
import responses

class TestNotifications(unittest.TestCase):

    def setUp(self) -> None:
        self.msg = "Hello"

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
