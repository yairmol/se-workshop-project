from domain.notifications.notifications import Notifications
from domain.token_module.tokenizer import Tokenizer
from domain.authentication_module.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from service.system_service import SystemService
from test_utils import NotificationMock


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
    def get_system_service():
        Notifications.set_communication(NotificationMock)
        return SystemService(
            Driver.get_commerce_system_facade(),
            Driver.get_tokenizer()
        )
