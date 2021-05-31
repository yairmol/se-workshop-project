import unittest

from domain.authentication_module.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.notifications.notifications import Notifications
from domain.token_module.tokenizer import Tokenizer
from service.system_service import SystemService


class TestService(unittest.TestCase):
    def setUp(self) -> None:
        self.service = SystemService(CommerceSystemFacade(Authenticator(), Notifications()), Tokenizer())

    def test_register1(self):
        token = self.service.enter()["result"]
        assert self.service.register(token, "aviv", "123456")["status"]

    def test_register2(self):
        token = self.service.enter()["result"]
        assert not self.service.register(token, "aviv", "123456789012345678901234567890")["status"]

    def test_register3(self):
        token = self.service.enter()["result"]
        self.service.exit(token)
        assert not self.service.register(token, "aviv", "1234567890")["status"]

    def test_log_in1(self):
        token = self.service.enter()["result"]
        self.service.register(token, "aviv", "123456")
        assert self.service.login(token, "aviv", "123456")["status"]

    def test_logout1(self):
        token = self.service.enter()["result"]
        self.service.register(token, "aviv", "123456")
        self.service.login(token, "aviv", "123456")
        assert self.service.logout(token)["status"]
