from domain.notifications.notifications import Notifications
from domain.token_module.tokenizer import Tokenizer
from domain.authentication_module.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.ifacade import ICommerceSystemFacade
from service.system_service import SystemService


class Driver:
    @staticmethod
    def get_commerce_system_facade() -> CommerceSystemFacade:
        return CommerceSystemFacade(Driver.get_authenticator(), Notifications())

    @staticmethod
    def get_authenticator():
        return Authenticator()

    @staticmethod
    def get_tokenizer():
        return Tokenizer()

    @staticmethod
    def get_system_service():
        return SystemService(
            Driver.get_commerce_system_facade(),
            Driver.get_tokenizer()
        )
