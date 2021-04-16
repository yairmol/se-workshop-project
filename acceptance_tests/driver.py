from acceptance_tests.facade_proxy import CommerceSystemFacadeProxy
from domain.auth.authenticator import Authenticator
from domain.commerce_system.facade import ICommerceSystemFacade
from service.system_service import SystemService


class Driver:
    @staticmethod
    def get_commerce_system_facade() -> ICommerceSystemFacade:
        return CommerceSystemFacadeProxy()

    @staticmethod
    def get_authenticator():
        return Authenticator()

    @staticmethod
    def get_system_service():
        return SystemService(
            Driver.get_commerce_system_facade(),
            Driver.get_authenticator()
        )
