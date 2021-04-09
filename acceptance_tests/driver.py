import acceptance_tests.facade_proxy as fp


class Driver:
    @staticmethod
    def get_commerce_system_facade() -> fp.ICommerceSystemFacade:
        return fp.CommerceSystemFacadeProxy()
