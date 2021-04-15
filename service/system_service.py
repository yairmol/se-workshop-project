from domain.auth.authenticator import Authenticator
from domain.commerce_system.commerceSystemFacade import CommerceSystemFacade
from domain.commerce_system.facade import ICommerceSystemFacade
from domain.commerce_system.user_managment import UserManagement


class SystemService:

    def __init__(self, commerce_system_facade: CommerceSystemFacade, authenticator: Authenticator):
        self.commerce_system_facade = commerce_system_facade
        self.authenticator = authenticator
        # self.user_management = UserManagement(Authenticator())

    def enter(self) -> str:  # returns the new user's token
        new_user_id = self.commerce_system_facade.enter()
        token = self.authenticator.add_new_user_token(new_user_id)
        return token

    def exit(self, token: str) -> None:
        user_id = self.authenticator.get_id_by_token(token)
        try:
            if self.authenticator.is_token_expired(token):
                raise Exception("User: " + str(user_id) + " Token's is not valid")
            self.authenticator.remove_token(token)
        except Exception as e:
            print(e)
        finally:
            if user_id > 0:
                self.commerce_system_facade.remove_active_user(user_id)

    def register(self, token: str, username: str, password: str, **more):
        user_id = self.authenticator.get_id_by_token(token)
        try:
            if self.authenticator.is_token_expired(token):
                raise Exception("User: " + str(user_id) + " Token's is not valid")
            self.commerce_system_facade.register(user_id, username, password, **more)
            print("LOG: Registered Successfully")
        except AssertionError as e:
            print(e)
            if user_id > 0:
                self.commerce_system_facade.remove_active_user(user_id)
