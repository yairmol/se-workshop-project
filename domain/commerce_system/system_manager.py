
class SystemManager:
    def __init__(self):
        raise NotImplementedError()

    def get_shop_transactions(self, store_credentials: dict) -> bool:
        raise NotImplementedError()

    def get_user_transactions(self):
        raise NotImplementedError()
