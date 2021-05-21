from typing import List, Union

from domain.authentication_module.authenticator import Authenticator
from domain.discount_module.discount_management import SimpleCond, DiscountDict, CompositeDiscountDict
from domain.notifications.notifications import Notifications
from domain.token_module.tokenizer import Tokenizer
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.logger.log import event_logger, error_logger


def make_status_dict(status: bool, desc: str, result) -> dict:
    return {'status': status, 'description': desc, 'result': result}


def handle_assertion(e: AssertionError):
    event_logger.warning(e)
    return make_status_dict(False, str(e), "")


def handle_exception(e: Exception):
    error_logger.error(e)
    return make_status_dict(False, "Server Error", "")


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
                CommerceSystemFacade(Authenticator(), Notifications()), Tokenizer()
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
    def enter(self) -> dict:  # returns the new user's token
        try:
            new_user_id = self.commerce_system_facade.enter()
            event_logger.info(f"A User entered the system, got id: {new_user_id}")
            token = self.tokenizer.add_new_user_token(new_user_id)
            withId = make_status_dict(True, "", token)
            withId["id"] = new_user_id
            return withId
        except Exception as e:
            return handle_exception(e)

    # 2.2
    def exit(self, token: str) -> dict:
        ret = False
        user_id = self.tokenizer.get_id_by_token(token)
        try:
            if self.tokenizer.is_token_expired(token):
                raise Exception(f"User: {user_id} Token's is not valid")
            self.tokenizer.remove_token(token)
            event_logger.info(f"User {user_id} exit the system")
            ret = make_status_dict(True, "", "")
        except Exception as e:
            return handle_exception(e)
        finally:
            if user_id > 0:
                self.commerce_system_facade.remove_active_user(user_id)
            return ret

    # 2.3
    def register(self, token: str, username: str, password: str, **more) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to register with username: {username}")
                self.commerce_system_facade.register(user_id, username, password, **more)
                event_logger.info(f"User: {user_id} Registered Successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 2.4
    def login(self, token: str, username: str, password: str) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to login with username: {username}")
                self.commerce_system_facade.login(user_id, username, password)
                event_logger.info(f"User: {user_id} Logged in Successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    def get_user_data(self, token: str) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to get user data")
                data = self.commerce_system_facade.get_user_data(user_id)
                return make_status_dict(True, "", data)
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 2.5
    def get_shop_info(self, token: str, shop_id: int) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user_sess {user_id} requested for shop {shop_id} information")
                return make_status_dict(True, "", self.commerce_system_facade.get_shop_info(shop_id))
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    def get_all_shops_info(self, token: str) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user_sess {user_id} requested for all shops information")
                return make_status_dict(True, "", self.commerce_system_facade.get_all_shop_info())
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 2.6
    def search_products(
            self, token, product_name: str = None, keywords: List[str] = None,
            categories: List[str] = None, filters: List[dict] = None
    ) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user_sess {user_id} requested for all shops information")
                return make_status_dict(
                    True, "", self.commerce_system_facade.search_products(
                        product_name, keywords, categories, filters
                    )
                )
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    def get_all_categories(self, token) -> dict:
        return make_status_dict(True, "", self.commerce_system_facade.get_all_categories())

    # 2.7
    def save_product_to_cart(self, token: str, shop_id: int, product_id: int, amount_to_buy: int) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to save {amount_to_buy}"
                                  f" products: {str(product_id)} of shop_id: {str(shop_id)}")
                self.commerce_system_facade.save_product_to_cart(user_id, shop_id, product_id, amount_to_buy)
                event_logger.info(f"User: {user_id} successfully save the product {product_id}")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 2.8
    def get_cart_info(self, token: str) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to get his cart info")
                ret = self.commerce_system_facade.get_cart_info(user_id)
                event_logger.info(f"User: {user_id} successfully got his cart")
                return make_status_dict(True, "", ret)
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 2.8
    def remove_product_from_cart(self, token: str, shop_id: int, product_id: int, amount: int) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to remove {str(amount)} "
                                  f"products: {str(product_id)} of shop_id: {str(shop_id)}")
                self.commerce_system_facade.remove_product_from_cart(user_id, shop_id, product_id, amount)
                event_logger.info(f"User: {user_id} successfully save the product {product_id}")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 2.9
    def purchase_product(self, token: str, shop_id: int, product_id: int,
                         amount_to_buy: int, payment_details: dict, delivery_details: dict) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to purchase {str(amount_to_buy)}"
                                  f" products: {str(product_id)} of shop_id: {str(shop_id)}")
                self.commerce_system_facade.purchase_product(
                    user_id, shop_id, product_id, amount_to_buy, payment_details, delivery_details
                )
                event_logger.info(f"User: {str(user_id)} successfully purchased the product {str(product_id)}")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            # except Exception as e:
            #     return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 2.9
    def purchase_shopping_bag(self, token: str, shop_id: int, payment_details: dict, delivery_details: dict) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to purchase {str(shop_id)} bag")
                self.commerce_system_facade.purchase_shopping_bag(user_id, shop_id, payment_details, delivery_details)
                event_logger.info(f"User: {user_id} successfully purchased the bag of the shop {str(shop_id)}")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 2.9
    def purchase_cart(self, token: str, payment_details: dict, delivery_details: dict,
                      all_or_nothing: bool = False) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {str(user_id)} tries to purchase his cart")
                self.commerce_system_facade.purchase_cart(user_id, payment_details, delivery_details, all_or_nothing)
                event_logger.info(f"User: {user_id} successfully purchased his cart")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 3. Subscriber Requirements

    # 3.1
    def logout(self, token: str) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                self.commerce_system_facade.logout(user_id)
                event_logger.info(f"User: {user_id} Logged Out Successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 3.2
    def open_shop(self, token: str, **shop_details) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to open shop: {shop_details['shop_name']}")
                shop_id = self.commerce_system_facade.open_shop(user_id, **shop_details)
                event_logger.info(f"User: {user_id} opened shop: {shop_id} successfully")
                return make_status_dict(True, "", shop_id)
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 3.7
    def get_personal_purchase_history(self, token: str) -> dict:

        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to get_personal_purchase_history")
                history = self.commerce_system_facade.get_personal_purchase_history(user_id)
                event_logger.info(f"User: {user_id} got personal purchase history successfully")
                return make_status_dict(True, "", history)
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4. Shop Owner Requirements

    # 4.1
    def add_product_to_shop(self, token: str, shop_id: int, **product_info) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to add product to shop {shop_id}")
                pid = self.commerce_system_facade.add_product_to_shop(user_id, shop_id, **product_info)
                event_logger.info(f"User: {user_id} added product successfully")
                return make_status_dict(True, "", pid)
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.1
    def edit_product_info(
            self, token: str, shop_id: int, product_id: int,
            product_name: str = None, description: str = None,
            price: float = None, quantity: int = None, categories: List[str] = None
    ) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to edit product info of "
                                  f"shop_id: {shop_id} product_id: {product_id}")
                self.commerce_system_facade.edit_product_info(
                    user_id, shop_id, product_id, product_name, description, price, quantity, categories
                )
                event_logger.info(f"User: {user_id} Edit product info successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.1
    def delete_product(self, token: str, shop_id: int, product_id: int) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to delete product of "
                                  f"shop_id: {shop_id} product_id: {product_id}")
                self.commerce_system_facade.delete_product(user_id, shop_id, product_id)
                event_logger.info("User: " + str(user_id) + " Delete product info successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.2
    def add_purchase_condition(self, token: str, shop_id: int, **condition_dict):
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to add purchase condition "
                                  f"shop_id: {shop_id}")
                self.commerce_system_facade.add_purchase_condition(user_id, shop_id,  **condition_dict)
                event_logger.info("User: " + str(user_id) + " added condition successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.2
    def remove_purchase_condition(self, token: str, shop_id: int, condition_id: int):
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to remove purchase condition "
                                  f"{condition_id} from"
                                  f"shop_id: {shop_id}")
                self.commerce_system_facade.remove_purchase_condition(user_id, shop_id, condition_id)
                event_logger.info("User: " + str(user_id) + " removed condition successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                event_logger.warning(e)
            except Exception as e:
                error_logger.error(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.5
    def appoint_shop_manager(self, token: str, shop_id: int, username: str, permissions: List[str]) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User:  {user_id} tries to appoint manager: {username} to shop_id: {shop_id}")
                self.commerce_system_facade.appoint_shop_manager(user_id, shop_id, username, permissions)
                event_logger.info(f"User: {user_id} Appointed shop manager: {username} successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.3
    def appoint_shop_owner(self, token: str, shop_id: int, username: str) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to appoint owner: {username} to shop_id: {shop_id}")
                self.commerce_system_facade.appoint_shop_owner(user_id, shop_id, username)
                event_logger.info(f"User: {user_id} Appointed shop owner: {username} successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.3
    def promote_shop_owner(self, token: str, shop_id: int, username: str) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to promote owner: {username} of shop_id: {shop_id}")
                self.commerce_system_facade.promote_shop_owner(user_id, shop_id, username)
                event_logger.info(f"User: {user_id} promoted shop owner: {username} successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.6
    def edit_manager_permissions(self, token: str, shop_id: int, username: str, permissions: List[str]) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to edit manager "
                                  f"permissions of: {username} in shop_id: {shop_id}")
                self.commerce_system_facade.edit_manager_permissions(user_id, shop_id, username, permissions)
                event_logger.info(f"User: {user_id} Edited manager: {username} permissions successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.7
    def un_appoint_manager(self, token: str, shop_id: int, username: str) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to un appoint manager: {username} of shop_id: {shop_id}")
                self.commerce_system_facade.unappoint_shop_manager(user_id, shop_id, username)
                event_logger.info(f"User: {user_id} Un appointed manager: {username} successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.7
    def un_appoint_shop_owner(self, token: str, shop_id: int, username: str) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to un appoint owner: {username} of shop_id: {shop_id}")
                self.commerce_system_facade.unappoint_shop_owner(user_id, shop_id, username)
                event_logger.info(f"User: {user_id} Un appointed owner: {username} successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.9
    def get_shop_staff_info(self, token: str, shop_id: int) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user {user_id} requested for shop {shop_id} staff information")
                return make_status_dict(True, "", self.commerce_system_facade.get_shop_staff_info(user_id, shop_id))
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 4.11
    def get_shop_transaction_history(self, token: str, shop_id: int) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user {user_id} requested for shop {shop_id} transaction history")
                return make_status_dict(True, "",
                                        self.commerce_system_facade.get_shop_transaction_history(user_id, shop_id))
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    # 6. System Administrator Requirements

    # 6.4
    def get_system_transactions(self, token: str):
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user {user_id} requested for the system transaction history")
                return make_status_dict(True, "", self.commerce_system_facade.get_system_transaction_history(user_id))
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    def get_product_info(self, token, shop_id: int, product_id: int) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"user {user_id} requested for product {product_id} info page")
                return make_status_dict(True, "", self.commerce_system_facade.get_product_info(shop_id, product_id))
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    def get_permissions(self, token, shop_id: int) -> dict:  # [permission: str, bool]
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                return make_status_dict(True, "", self.commerce_system_facade.get_permissions(user_id, shop_id))
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    def get_discounts(self, token: str, shop_id: int) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to get the discounts of shop: {shop_id}")
                ret = self.commerce_system_facade.get_discounts(user_id, shop_id)
                event_logger.info(f"User: {user_id} got discounts of shop: {shop_id} successfully")
                return make_status_dict(True, "", ret)
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", [])

    def add_discount(self, token: str, shop_id: int, has_cond: bool, condition: List[Union[str, SimpleCond, List]],
                     discount: Union[DiscountDict, CompositeDiscountDict]) -> dict:
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to add discount to shop: {shop_id}")
                discount_id = self.commerce_system_facade.add_discount(user_id, shop_id, has_cond, condition, discount)
                event_logger.info(f"User: {user_id} added discount to shop: {shop_id} successfully")
                return make_status_dict(True, "", discount_id)
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    def aggregate_discounts(self, token: str, shop_id: int, discount_ids: List[int], operator: str):
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to aggregate discounts to shop: {shop_id}")
                self.commerce_system_facade.aggregate_discounts(user_id, shop_id, discount_ids, operator)
                event_logger.info(f"User: {user_id} aggregated discounts to shop: {shop_id} successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    def move_discount_to(self, token: str, shop_id: int, src_discount_id: int, dst_discount_id: int):
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to move discounts in shop: {shop_id}")
                self.commerce_system_facade.move_discount_to(user_id, shop_id, src_discount_id, dst_discount_id)
                event_logger.info(f"User: {user_id} moved discounts in shop: {shop_id} successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    def delete_discounts(self, token: str, shop_id, discount_ids: List[int]):
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to delete discounts to shop: {shop_id}")
                self.commerce_system_facade.delete_discounts(user_id, shop_id, discount_ids)
                event_logger.info(f"User: {user_id} deleted discounts to shop: {shop_id} successfully")
                return make_status_dict(True, "", "")
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    def get_user_appointemnts(self, token):
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                event_logger.info(f"User: {user_id} tries to get his appointments")
                res = self.commerce_system_facade.get_user_appointments(user_id)
                event_logger.info(f"User: {user_id} got his appointments successfully")
                return make_status_dict(True, "", res)
            except AssertionError as e:
                return handle_assertion(e)
            except Exception as e:
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    def cleanup(self):
        self.commerce_system_facade.clean_up()
