import unittest
from unittest.mock import MagicMock

from domain.authentication_module.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from service.system_service import SystemService


class TestService(unittest.TestCase):

    def test_register1(self):
        service = SystemService(CommerceSystemFacade(), Authenticator())
        token = service.enter()
        assert service.register(token, "aviv", "123456")

    def test_register2(self):
        service = SystemService(CommerceSystemFacade(), Authenticator())
        token = service.enter()
        assert not service.register(token, "aviv", "123456789012345678901234567890")

    def test_register3(self):
        service = SystemService(CommerceSystemFacade(), Authenticator())
        token = service.enter()
        service.exit(token)
        assert not service.register(token, "aviv", "1234567890")

    def test_log_in1(self):
        service = SystemService(CommerceSystemFacade(), Authenticator())
        token = service.enter()
        service.register(token, "aviv", "123456")
        assert service.login(token,"aviv", "123456")

    def test_logout1(self):
        service = SystemService(CommerceSystemFacade(), Authenticator())
        token = service.enter()
        service.register(token, "aviv", "123456")
        service.login(token, "aviv", "123456")
        assert service.logout(token)
