from typing import List

from domain.auth.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade


class SystemService:

    def __init__(self, commerce_system_facade: CommerceSystemFacade, authenticator: Authenticator):
        self.commerce_system_facade = commerce_system_facade
        self.authenticator = authenticator

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

    def register(self, token: str, username: str, password: str, **more)-> bool:
        user_id = self.authenticator.get_id_by_token(token)
        try:
            if self.authenticator.is_token_expired(token):
                raise TokenNotValidException("User Token's Expired")
            self.commerce_system_facade.register(user_id, username, password, **more)
            print("LOG: User: " + str(user_id) + " Registered Successfully")
            return True
        except TokenNotValidException as e:
            print(e)
            if user_id > 0:
                self.commerce_system_facade.remove_active_user(user_id)
            return False
        except AssertionError as e:
            print(e)
            return False

    def login(self, token: str, username: str, password: str)-> bool:
        user_id = self.authenticator.get_id_by_token(token)
        try:
            if self.authenticator.is_token_expired(token):
                raise TokenNotValidException("User Token's Expired")
            self.commerce_system_facade.login(user_id, username, password)
            print("LOG: User: " + str(user_id) + " Logged in Successfully")
            return True
        except TokenNotValidException as e:
            print(e)
            if user_id > 0:
                self.commerce_system_facade.remove_active_user(user_id)
            return False
        except AssertionError as e:
            print(e)
            return False

    def logout(self, token: str)-> bool:
        user_id = self.authenticator.get_id_by_token(token)
        try:
            if self.authenticator.is_token_expired(token):
                raise TokenNotValidException("User Token's Expired")
            self.commerce_system_facade.logout(user_id)
            print("LOG: User: " + str(user_id) + " Logged out Successfully")
            return True
        except TokenNotValidException as e:
            print(e)
            if user_id > 0:
                self.commerce_system_facade.remove_active_user(user_id)
            return False
        except AssertionError as e:
            print(e)
            return False

    def search_products(
            self, product_name: str = None, keywords: List[str] = None,
            categories: List[str] = None, filters: List[dict] = None
    ) -> List[dict]:
        """
        :param categories:
        :param product_name: product name (optional)
        :param keywords:  OR keywords and categories separated by spaces
        :param filters: a list of filters where a filter is a dictionary containing a key 'type' and additional keys
        according to type.
        :return: returns the results as a list of dictionaries
        """
        return self.commerce_system_facade.search_products(product_name, keywords, categories, filters)


class TokenNotValidException(Exception):
    pass
