from domain.auth.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.commerce_system.ifacade import ICommerceSystemFacade
from service.system_service import SystemService


class Driver:
    @staticmethod
    def get_commerce_system_facade() -> CommerceSystemFacade:
        return CommerceSystemFacade()

    @staticmethod
    def get_authenticator():
        return Authenticator()

    @staticmethod
    def get_system_service():
        return SystemService(
            Driver.get_commerce_system_facade(),
            Driver.get_authenticator()
        )
