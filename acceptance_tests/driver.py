from acceptance_tests.facade_proxy import CommerceSystemFacadeProxy
from domain.commerce_system.facade import ICommerceSystemFacade


class Driver:
    @staticmethod
    def get_commerce_system_facade() -> ICommerceSystemFacade:
        return CommerceSystemFacadeProxy()
