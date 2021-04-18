from typing import List

from domain.auth.authenticator import Authenticator
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.logger.log import event_logger, error_logger


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
        try:
            new_user_id = self.commerce_system_facade.enter()
            event_logger.info("A User entered the system, got id: " + str(new_user_id))
            token = self.authenticator.add_new_user_token(new_user_id)
            return token
        except Exception as e:
            error_logger.error(e)

    def exit(self, token: str) -> bool:
        ret = False
        user_id = self.authenticator.get_id_by_token(token)
        try:
            if self.authenticator.is_token_expired(token):
                raise Exception("User: " + str(user_id) + " Token's is not valid")
            self.authenticator.remove_token(token)
            event_logger.info("User " + str(user_id) + " exit the system")
            ret = True
        except Exception as e:
            error_logger.error(e)
        finally:
            if user_id > 0:
                self.commerce_system_facade.remove_active_user(user_id)
            return ret

    def register(self, token: str, username: str, password: str, **more) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info("User: " + str(user_id) +
                                  " tries to register with username: " + username + "password: " + password)
                self.commerce_system_facade.register(user_id, username, password, **more)
                event_logger.info("User: " + str(user_id) + " Registered Successfully")
                return True
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def login(self, token: str, username: str, password: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info("User: " + str(user_id) +
                                  " tries to login with username: " + username + "password: " + password)
                self.commerce_system_facade.login(user_id, username, password)
                event_logger.info("User: " + str(user_id) + " Logged in Successfully")
                return True
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def logout(self, token: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                self.commerce_system_facade.logout(user_id)
                event_logger.info("LOG: User: " + str(user_id) + " Logged Out Successfully")
                return True
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    """NEEDS TO BE CHANGED - HANDLE TRANSPORTING PRODUCT DATA DIFFERENTLY"""

    # def add_product_to_shop(self, user_id: int, shop_id: str, product: Product) -> int:
    #     pass

    def edit_product_info(self, token: str, shop_id: str, product_id: int, **product_info) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info("User: " + str(user_id) +
                                  " tries to edit product info of shop_id: " + shop_id + "product_id: " + str(
                    product_id))
                self.commerce_system_facade.edit_product_info(user_id, shop_id, product_id, product_info)
                event_logger.info("User: " + str(user_id) + " Edit product info successfully")
                return True
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def delete_product(self, token: str, shop_id: str, product_id: int) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info("User: " + str(user_id) +
                                  " tries to delete product of shop_id: " + shop_id + "product_id: " + str(product_id))
                self.commerce_system_facade.delete_product(user_id, shop_id, product_id)
                event_logger.info("User: " + str(user_id) + " Delete product info successfully")
                return True
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def appoint_shop_manager(self, token: str, shop_id: int, username: str, permissions: List[str]) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info("User: " + str(user_id) +
                                  " tries to appoint manager: " + username + " to shop_id: " + str(shop_id))
                self.commerce_system_facade.appoint_shop_manager(user_id, shop_id, username, permissions)
                event_logger.info("User: " + str(user_id) + " Appointed shop manager: " + username + " successfully")
                return True
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def appoint_shop_owner(self, token: str, shop_id: int, username: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info("User: " + str(user_id) +
                                  " tries to appoint owner: " + username + " to shop_id: " + str(shop_id))
                self.commerce_system_facade.appoint_shop_owner(user_id, shop_id, username)
                event_logger.info("User: " + str(user_id) + " Appointed shop owner: " + username + " successfully")
                return True
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def promote_shop_owner(self, token: str, shop_id: int, username: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info("User: " + str(user_id) +
                                  " tries to promote owner: " + username + " of shop_id: " + str(shop_id))
                self.commerce_system_facade.promote_shop_owner(user_id, shop_id, username)
                event_logger.info("User: " + str(user_id) + " promoted shop owner: " + username + " successfully")
                return True
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def edit_manager_permissions(self, token: str, shop_id: int, username: str, permissions: List[str]) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info("User: " + str(user_id) +
                                  " tries to edit manager permissions of: " + username + " in shop_id: " + str(shop_id))
                self.commerce_system_facade.edit_manager_permissions(user_id, shop_id, username, permissions)
                event_logger.info(
                    "User: " + str(user_id) + " Edited manager: " + username + " permissions successfully")
                return True
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def un_appoint_manager(self, token: str, shop_id: int, username: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info("User: " + str(user_id) +
                                  " tries to un appoint manager: " + username + " of shop_id: " + str(shop_id))
                self.commerce_system_facade.un_appoint_manager(user_id, shop_id, username)
                event_logger.info("User: " + str(user_id) + " Un appointed manager: " + username + " successfully")
                return True
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def open_shop(self, token: str, **shop_details) -> int:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info("User: " + str(user_id) +
                                  " tries to open shop: " + str(shop_details["shop_name"]))
                shop_id = self.commerce_system_facade.open_shop(user_id, **shop_details)
                event_logger.info("User: " + str(user_id) + " opend shop: " + str(shop_id) + " successfully")
                return shop_id
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def un_appoint_shop_owner(self, token: str, shop_id: int, username: str):
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info("User: " + str(user_id) +
                                  " tries to un appoint owner: " + username + " of shop_id: " + str(shop_id))
                self.commerce_system_facade.unappoint_shop_owner(user_id, shop_id, username)
                event_logger.info("User: " + str(user_id) + " Un appointed owner: " + username + " successfully")
                return True
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def get_shop_info(self, token: str, shop_id: int) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info(f"user_sess {user_id} requested for shop {shop_id} information")
                return self.commerce_system_facade.get_shop_info(shop_id)
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return {}
            except Exception as e:
                error_logger.error(e)
                return {}
        return {}

    def get_shop_staff_info(self, token: str, shop_id: int) -> List[dict]:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info(f"user {user_id} requested for shop {shop_id} staff information")
                return self.commerce_system_facade.get_shop_staff_info(shop_id)
            except AssertionError as e:
                print(e)
                event_logger.warning(e)
                return {}
            except Exception as e:
                error_logger.error(e)
                return {}
        return {}

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

    def get_personal_purchase_history(self, token: str) -> List[dict]:
        try:
            assert self.is_valid_token(token), f"Invalid user_sess token {token}"
            user_id = self.authenticator.get_id_by_token(token)
            return self.commerce_system_facade.get_personal_purchase_history(user_id)
        except AssertionError as e:
            event_logger.error(e)
        except Exception as e:
            error_logger.error(e)

    def save_product_to_cart(self, token: str, shop_id: str, product_id: int, amount_to_buy: int) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info(
                    f"User: {str(user_id)} tries to save {amount_to_buy} products: {str(product_id)}  of shop_id: {str(shop_id)}")
                self.commerce_system_facade.save_product_to_cart(user_id, shop_id, product_id, amount_to_buy)
                event_logger.info(f"User: {user_id} successfully save the product {product_id}")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def remove_product_from_cart(self, token: str, user_id: int, shop_id: int, product_id: int, amount: int) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info(
                    f"User: {str(user_id)} tries to remove {str(amount)}  products: {str(product_id)}  of shop_id: {str(shop_id)}")
                self.commerce_system_facade.remove_product_from_cart(user_id, shop_id, product_id, amount)
                event_logger.info(f"User: {user_id} successfully save the product {product_id}")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def purchase_product(self, token: str, shop_id: str, product_id: int, amount_to_buy: int, payment_details: dict):
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info(
                    f"User: {str(user_id)} tries to purchase {str(amount_to_buy)}  products: {str(product_id)}  of "
                    f"shop_id: {str(shop_id)}")
                self.commerce_system_facade.purchase_product(user_id, shop_id, product_id, amount_to_buy, payment_details)
                event_logger.info(f"User: {str(user_id)} successfully purchased the product {str(product_id)}")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def purchase_shopping_bag(self, token: str, shop_id: str, payment_details: dict):
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to purchase {str(shop_id)}  bag")
                self.commerce_system_facade.purchase_shopping_bag(user_id, shop_id, payment_details)
                event_logger.info(f"User: {user_id} successfully purchased the bag of the shop {str(shop_id)}")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def purchase_cart(self, token: str, shop_id: str, payment_details: dict, all_or_nothing: bool):
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to purchase his cart")
                self.commerce_system_facade.purchase_cart(user_id, payment_details, all_or_nothing)
                event_logger.info(f"User: {user_id} successfully purchased his cart")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    def get_cart_info(self, token: str):
        if self.is_valid_token(token):
            try:
                user_id = self.authenticator.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to get his cart info")
                self.commerce_system_facade.get_cart_info(user_id)
                event_logger.info(f"User: {user_id} successfully got his cart")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

