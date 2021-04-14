
class Subscribed:
    def _init_(self, username: str):
        self.appointments = []
        self.username = username

    def open_store(self, store_credentials: dict) -> bool:
        raise NotImplementedError()

    def get_transaction_history(self):
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()
