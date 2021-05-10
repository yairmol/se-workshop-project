from acceptance_tests.mocks import NotificationsMock
from domain.token_module.tokenizer import Tokenizer
from domain.authentication_module.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.ifacade import ICommerceSystemFacade
from service.system_service import SystemService


class Driver:
    @staticmethod
    def get_commerce_system_facade() -> CommerceSystemFacade:
        return CommerceSystemFacade(Driver.get_authenticator())

    @staticmethod
    def get_authenticator():
        return Authenticator()

    @staticmethod
    def get_tokenizer():
        return Tokenizer()

    @staticmethod
    def get_notifications():
        return NotificationsMock()

    @staticmethod
    def get_system_service():
        return SystemService(
            Driver.get_commerce_system_facade(),
            Driver.get_tokenizer(),
            Driver.get_notifications()
        )
