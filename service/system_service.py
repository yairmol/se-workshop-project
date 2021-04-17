from typing import List

from domain.auth.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade


class TokenNotValidException(Exception):
    pass


class SystemService:

    def __init__(self, commerce_system_facade: CommerceSystemFacade, authenticator: Authenticator):
        self.commerce_system_facade = commerce_system_facade
        self.authenticator = authenticator

    def is_valid_token(self, token: str):
        if self.authenticator.is_token_expired(token):
            user_id = self.authenticator.get_id_by_token(token)
            if user_id > 0:
                self.commerce_system_facade.remove_active_user(user_id)
            return False
        return True

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

    def register(self, token: str, username: str, password: str, **more) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                self.commerce_system_facade.register(user_id, username, password, **more)
                print("LOG: User: " + str(user_id) + " Registered Successfully")
                return True
            except AssertionError as e:
                print(e)
                return False
        print("User Token's Expired")
        return False

    def login(self, token: str, username: str, password: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                self.commerce_system_facade.login(user_id, username, password)
                print("LOG: User: " + str(user_id) + " Logged in Successfully")
                return True
            except AssertionError as e:
                print(e)
                return False
        return False

    def logout(self, token: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                self.commerce_system_facade.logout(user_id)
                print("LOG: User: " + str(user_id) + " Logged Out Successfully")
                return True
            except AssertionError as e:
                print(e)
                return False
        return False

    """NEEDS TO BE CHANGED - HANDLE TRANSPORTING PRODUCT DATA DIFFERENTLY"""

    # def add_product_to_shop(self, user_id: int, shop_id: str, product: Product) -> int:
    #     pass

    def edit_product_info(self, token: str, shop_id: str, product_id: int, **product_info) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                self.commerce_system_facade.edit_product_info(user_id, shop_id, product_id, product_info)
                print("LOG: User: " + str(user_id) + " Edit product info successfully")
                return True
            except AssertionError as e:
                print(e)
                return False
        return False

    def delete_product(self, token: str, shop_id: str, product_id: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                self.commerce_system_facade.delete_product(user_id, shop_id, product_id)
                print("LOG: User: " + str(user_id) + " Delete product info successfully")
                return True
            except AssertionError as e:
                print(e)
                return False
        return False

    def appoint_shop_manager(self, token: str, shop_id: int, username: str, permissions: List[str]) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                self.commerce_system_facade.appoint_shop_manager(user_id, shop_id, username, permissions)
                print("LOG: User: " + str(user_id) + " Appointed shop manager: " + username + " successfully")
                return True
            except AssertionError as e:
                print(e)
                return False
        return False

    def appoint_shop_owner(self, token: str, shop_id: int, username: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                self.commerce_system_facade.appoint_shop_owner(user_id, shop_id, username)
                print("LOG: User: " + str(user_id) + " Appointed shop owner: " + username + " successfully")
                return True
            except AssertionError as e:
                print(e)
                return False
        return False

    def edit_manager_permissions(self, token: str, shop_id: int, username: str, permissions: List[str]) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                self.commerce_system_facade.edit_manager_permissions(user_id, shop_id, username, permissions)
                print("LOG: User: " + str(user_id) + " Edited manager: " + username + " permissions successfully")
                return True
            except AssertionError as e:
                print(e)
                return False
        return False

    def un_appoint_manager(self, token: str, shop_id: int, username: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                self.commerce_system_facade.un_appoint_manager(user_id, shop_id, username)
                print("LOG: User: " + str(user_id) + " Un appointed manager: " + username + " successfully")
                return True
            except AssertionError as e:
                print(e)
                return False
        return False

    def un_appoint_shop_owner(self, token: str, shop_id: int, username: str):
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                self.commerce_system_facade.unappoint_shop_owner(user_id, shop_id, username)
                print("LOG: User: " + str(user_id) + " Un appointed owner: " + username + " successfully")
                return True
            except AssertionError as e:
                print(e)
                return False
        return False
