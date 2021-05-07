from typing import List, Union

from domain.authentication_module.authenticator import Authenticator
from domain.discount_module.discount_management import SimpleCond, DiscountDict
from domain.token_module.tokenizer import Tokenizer
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.logger.log import event_logger, error_logger


class TokenNotValidException(Exception):
    pass


class SystemService:
    __instance = None

    def __init__(self, commerce_system_facade: CommerceSystemFacade, tokenizer: Tokenizer):
        self.commerce_system_facade = commerce_system_facade
        self.tokenizer = tokenizer
        self.commerce_system_facade.create_admin_user()

    @classmethod
    def get_system_service(cls):
        if not SystemService.__instance:
            SystemService.__instance = SystemService(
                CommerceSystemFacade(Authenticator()), Tokenizer()
            )
        return SystemService.__instance

    def is_valid_token(self, token: str):
        if self.tokenizer.is_token_expired(token):
            user_id = self.tokenizer.get_id_by_token(token)
            if user_id > 0:
                self.commerce_system_facade.remove_active_user(user_id)
            return False
        return True

    # 2.1
    def enter(self) -> str:  # returns the new user's token
        try:
            new_user_id = self.commerce_system_facade.enter()
            event_logger.info(f"A User entered the system, got id: {new_user_id}")
            token = self.tokenizer.add_new_user_token(new_user_id)
            return token
        except Exception as e:
            error_logger.error(e)

    # 2.2
    def exit(self, token: str) -> bool:
        ret = False
        user_id = self.tokenizer.get_id_by_token(token)
        try:
            if self.tokenizer.is_token_expired(token):
                raise Exception(f"User: {user_id} Token's is not valid")
            self.tokenizer.remove_token(token)
            event_logger.info(f"User {user_id} exit the system")
            ret = True
        except Exception as e:
            error_logger.error(e)
        finally:
            if user_id > 0:
                self.commerce_system_facade.remove_active_user(user_id)
            return ret

    # 2.3
    def register(self, token: str, username: str, password: str, **more) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to register with username: {username}")
                self.commerce_system_facade.register(user_id, username, password, **more)
                event_logger.info(f"User: {user_id} Registered Successfully")
                return True
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return False

    # 2.4
    def login(self, token: str, username: str, password: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to login with username: {username}")
                self.commerce_system_facade.login(user_id, username, password)
                event_logger.info(f"User: {user_id} Logged in Successfully")
                return True
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return False

    # 2.5
    def get_shop_info(self, token: str, shop_id: int) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user_sess {user_id} requested for shop {shop_id} information")
                return self.commerce_system_facade.get_shop_info(shop_id)
            except AssertionError as e:
                event_logger.warning(e)
                return {}
            except Exception as e:
                error_logger.error(e)
                return {}
        return {}

    def get_all_shops_info(self, token: str) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user_sess {user_id} requested for all shops information")
                return self.commerce_system_facade.get_all_shop_info()
            except AssertionError as e:
                event_logger.warning(e)
                return {}
            except Exception as e:
                error_logger.error(e)
                return {}
        return {}
    # 2.6
    def search_products(
            self, product_name: str = None, keywords: List[str] = None,
            categories: List[str] = None, filters: List[dict] = None
    ) -> List[dict]:
        return self.commerce_system_facade.search_products(product_name, keywords, categories, filters)

    # 2.7
    def save_product_to_cart(self, token: str, shop_id: int, product_id: int, amount_to_buy: int) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to save {amount_to_buy}"
                                  f" products: {str(product_id)} of shop_id: {str(shop_id)}")
                self.commerce_system_facade.save_product_to_cart(user_id, shop_id, product_id, amount_to_buy)
                event_logger.info(f"User: {user_id} successfully save the product {product_id}")
                return True
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return False

    # 2.8
    def get_cart_info(self, token: str) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to get his cart info")
                ret = self.commerce_system_facade.get_cart_info(user_id)
                event_logger.info(f"User: {user_id} successfully got his cart")
                return ret
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return {}

    # 2.8
    def remove_product_from_cart(self, token: str, shop_id: int, product_id: int, amount: int) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to remove {str(amount)} "
                                  f"products: {str(product_id)} of shop_id: {str(shop_id)}")
                self.commerce_system_facade.remove_product_from_cart(user_id, shop_id, product_id, amount)
                event_logger.info(f"User: {user_id} successfully save the product {product_id}")
                return True
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return False

    # 2.9
    def purchase_product(self, token: str, shop_id: int, product_id: int,
                         amount_to_buy: int, payment_details: dict) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to purchase {str(amount_to_buy)}"
                                  f" products: {str(product_id)} of shop_id: {str(shop_id)}")
                self.commerce_system_facade.purchase_product(
                    user_id, shop_id, product_id, amount_to_buy, payment_details
                )
                event_logger.info(f"User: {str(user_id)} successfully purchased the product {str(product_id)}")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    # 2.9
    def purchase_shopping_bag(self, token: str, shop_id: int, payment_details: dict) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to purchase {str(shop_id)} bag")
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

    # 2.9
    def purchase_cart(self, token: str, payment_details: dict, all_or_nothing: bool = False) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
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

    # 3. Subscriber Requirements

    # 3.1
    def logout(self, token: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                self.commerce_system_facade.logout(user_id)
                event_logger.info(f"User: {user_id} Logged Out Successfully")
                return True
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return False

    # 3.2
    def open_shop(self, token: str, **shop_details) -> int:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to open shop: {shop_details['shop_name']}")
                shop_id = self.commerce_system_facade.open_shop(user_id, **shop_details)
                event_logger.info(f"User: {user_id} opened shop: {shop_id} successfully")
                return shop_id
            except AssertionError as e:
                event_logger.warning(e)
                return -1
            except Exception as e:
                error_logger.error(e)
                return -1
        return -1

    # 3.7
    def get_personal_purchase_history(self, token: str) -> List[dict]:

        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to get_personal_purchase_history")
                history = self.commerce_system_facade.get_personal_purchase_history(user_id)
                event_logger.info(f"User: {user_id} got personal purchase history successfully")
                return history
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return []

    # 4. Shop Owner Requirements

    # 4.1
    def add_product_to_shop(self, token: str, shop_id: int, **product_info) -> int:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to add product to shop {shop_id}")
                pid = self.commerce_system_facade.add_product_to_shop(user_id, shop_id, **product_info)
                event_logger.info(f"User: {user_id} added product successfully")
                return pid
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return -1

    # 4.1
    def edit_product_info(
            self, token: str, shop_id: int, product_id: int,
            product_name: str = None, description: str = None,
            price: float = None, quantity: int = None, categories: List[str] = None
    ) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to edit product info of "
                                  f"shop_id: {shop_id} product_id: {product_id}")
                self.commerce_system_facade.edit_product_info(
                    user_id, shop_id, product_id, product_name, description, price, quantity, categories
                )
                event_logger.info(f"User: {user_id} Edit product info successfully")
                return True
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return False

    # 4.1
    def delete_product(self, token: str, shop_id: int, product_id: int) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to delete product of "
                                  f"shop_id: {shop_id} product_id: {product_id}")
                self.commerce_system_facade.delete_product(user_id, shop_id, product_id)
                event_logger.info("User: " + str(user_id) + " Delete product info successfully")
                return True
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return False

    # 4.5
    def appoint_shop_manager(self, token: str, shop_id: int, username: str, permissions: List[str]) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User:  {user_id} tries to appoint manager: {username} to shop_id: {shop_id}")
                self.commerce_system_facade.appoint_shop_manager(user_id, shop_id, username, permissions)
                event_logger.info(f"User: {user_id} Appointed shop manager: {username} successfully")
                return True
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return False

    # 4.3
    def appoint_shop_owner(self, token: str, shop_id: int, username: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to appoint owner: {username} to shop_id: {shop_id}")
                self.commerce_system_facade.appoint_shop_owner(user_id, shop_id, username)
                event_logger.info(f"User: {user_id} Appointed shop owner: {username} successfully")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    # 4.3
    def promote_shop_owner(self, token: str, shop_id: int, username: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to promote owner: {username} of shop_id: {shop_id}")
                self.commerce_system_facade.promote_shop_owner(user_id, shop_id, username)
                event_logger.info(f"User: {user_id} promoted shop owner: {username} successfully")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    # 4.6
    def edit_manager_permissions(self, token: str, shop_id: int, username: str, permissions: List[str]) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to edit manager "
                                  f"permissions of: {username} in shop_id: {shop_id}")
                self.commerce_system_facade.edit_manager_permissions(user_id, shop_id, username, permissions)
                event_logger.info(f"User: {user_id} Edited manager: {username} permissions successfully")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    # 4.7
    def un_appoint_manager(self, token: str, shop_id: int, username: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to un appoint manager: {username} of shop_id: {shop_id}")
                self.commerce_system_facade.unappoint_shop_manager(user_id, shop_id, username)
                event_logger.info(f"User: {user_id} Un appointed manager: {username} successfully")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    # 4.7
    def un_appoint_shop_owner(self, token: str, shop_id: int, username: str) -> bool:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to un appoint owner: {username} of shop_id: {shop_id}")
                self.commerce_system_facade.unappoint_shop_owner(user_id, shop_id, username)
                event_logger.info(f"User: {user_id} Un appointed owner: {username} successfully")
                return True
            except AssertionError as e:
                event_logger.warning(e)
                return False
            except Exception as e:
                error_logger.error(e)
                return False
        return False

    # 4.9
    def get_shop_staff_info(self, token: str, shop_id: int) -> List[dict]:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user {user_id} requested for shop {shop_id} staff information")
                return self.commerce_system_facade.get_shop_staff_info(user_id, shop_id)
            except AssertionError as e:
                event_logger.warning(e)
                return []
            except Exception as e:
                error_logger.error(e)
                return []
        return []

    # 4.11
    def get_shop_transaction_history(self, token: str, shop_id: int) -> List[dict]:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user {user_id} requested for shop {shop_id} transaction history")
                return self.commerce_system_facade.get_shop_transaction_history(user_id, shop_id)
            except AssertionError as e:
                event_logger.warning(e)
                return []
            except Exception as e:
                error_logger.error(e)
                return []
        return []

    # 6. System Administrator Requirements

    # 6.4
    def get_system_transactions(self, token: str):
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user {user_id} requested for the system transaction history")
                return self.commerce_system_facade.get_system_transaction_history(user_id)
            except AssertionError as e:
                event_logger.warning(e)
                return []
            except Exception as e:
                error_logger.error(e)
                return []
        return []

    def get_product_info(self, token, shop_id: int, product_id: int) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user {user_id} requested for product {product_id} info page")
                return self.commerce_system_facade.get_product_info(shop_id, product_id)
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return {}

    def get_permissions(self, token, shop_id: int) -> dict:  # [permission: str, bool]
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                return self.commerce_system_facade.get_permissions(user_id, shop_id)
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return {}

    ''' NEED TO ADD TOKEN CHECK... But Maybe token check will be moved to ABOVE layer '''
    def add_discount(self, token: str, shop_id: int, has_cond: bool, condition: List[Union[str,SimpleCond, List]], discount: DiscountDict):
        self.commerce_system_facade.add_discount(shop_id, has_cond, condition, discount)

    def aggregate_discounts(self, token:str, shop_id: int, discount_ids: [int], func: str):
        self.commerce_system_facade.aggregate_discounts(shop_id,discount_ids,func)

    def cleanup(self):
        self.commerce_system_facade.clean_up()
