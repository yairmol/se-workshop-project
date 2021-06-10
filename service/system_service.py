from typing import List, Union

from data_model import PurchaseTypeDict
from domain.authentication_module.authenticator import Authenticator
from domain.discount_module.discount_management import SimpleCond, DiscountDict, CompositeDiscountDict
from domain.token_module.tokenizer import Tokenizer
from domain.commerce_system.commerce_system_facade import CommerceSystemFacade
from domain.logger.log import event_logger, error_logger
from service.init_dict import InitDict


def make_status_dict(status: bool, desc: str, result) -> dict:
    return {'status': status, 'description': desc, 'result': result}


def handle_assertion(e: AssertionError):
    event_logger.warning(e)
    return make_status_dict(False, str(e), "")


def handle_exception(e: Exception):
    error_logger.error(e)
    return make_status_dict(False, "Server Error", "")


class InitError(Exception):
    pass


def handler(func):
    def inner(self, token, *args, **kwargs):
        if self.is_valid_token(token):
            try:
                user_id = self.tokenizer.get_id_by_token(token)
                return func(self, user_id, *args, **kwargs)
            except AssertionError as e:
                print("assertion", e)
                return handle_assertion(e)
            except Exception as e:
                print("error", e)
                return handle_exception(e)
        return make_status_dict(False, "Invalid Token", "")

    return inner


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

    def init(self, init: InitDict):
        bindings = dict()
        for action in init["actions"]:
            action_name = action["action"]
            user = action["user"]
            if action_name == "enter":
                bindings[user] = self.enter()["result"]
                continue
            params = action["params"]
            for param, val in params.items():
                if isinstance(val, dict) and "ref" in val:
                    params[param] = bindings[val["ref"]]
            ret = getattr(self, action_name)(token=bindings[user], **params)
            if not ret["status"]:
                raise InitError(ret["description"])
            if "ref_id" in action:
                bindings[action["ref_id"]] = ret["result"]
        return bindings

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
            self.commerce_system_facade.exit(user_id)
            ret = make_status_dict(True, "", "")
        except Exception as e:
            return handle_exception(e)
        finally:
            if user_id > 0:
                self.commerce_system_facade.remove_active_user(user_id)
            return make_status_dict(ret, "", "")

    # 2.3
    @handler
    def register(self, user_id: int, username: str, password: str, **more) -> dict:
        event_logger.info(f"User: {user_id} tries to register with username: {username}")
        self.commerce_system_facade.register(user_id, username, password, **more)
        event_logger.info(f"User: {user_id} Registered Successfully")
        return make_status_dict(True, "", "")

    # 2.4
    @handler
    def login(self, user_id: int, username: str, password: str) -> dict:
        event_logger.info(f"User: {user_id} tries to login with username: {username}")
        self.commerce_system_facade.login(user_id, username, password)
        event_logger.info(f"User: {user_id} Logged in Successfully")
        return make_status_dict(True, "", "")

    @handler
    def get_user_data(self, user_id: int) -> dict:
        event_logger.info(f"User: {user_id} tries to get user data")
        data = self.commerce_system_facade.get_user_data(user_id)
        return make_status_dict(True, "", data)

    # 2.5
    @handler
    def get_shop_info(self, user_id: int, shop_id: int) -> dict:
        event_logger.info(f"user_sess {user_id} requested for shop {shop_id} information")
        return make_status_dict(True, "", self.commerce_system_facade.get_shop_info(user_id, shop_id))

    @handler
    def get_offers(self, user_id: int, shop_id: int, product_id) -> dict:
        event_logger.info(f"user_sess {user_id} requested for shop {product_id} offers")
        return make_status_dict(True, "", self.commerce_system_facade.get_offers(user_id, shop_id, product_id))

    @handler
    def get_all_shops_info(self, user_id: int) -> dict:
        event_logger.info(f"user_sess {user_id} requested for all shops information")
        return make_status_dict(True, "", self.commerce_system_facade.get_all_shop_info())

    # 2.6
    @handler
    def search_products(
            self, user_id: int, product_name: str = None, keywords: List[str] = None,
            categories: List[str] = None, filters: List[dict] = None
    ) -> dict:
        event_logger.info(f"user_sess {user_id} requested for all shops information")
        return make_status_dict(
            True, "", self.commerce_system_facade.search_products(
                product_name, keywords, categories, filters
            )
        )

    @handler
    def get_all_categories(self, token) -> dict:
        return make_status_dict(True, "", self.commerce_system_facade.get_all_categories())

    # 2.7
    @handler
    def save_product_to_cart(self, user_id: int, shop_id: int, product_id: int, amount_to_buy: int,
                             purchase_type_id=None, **pt_args) -> dict:
        event_logger.info(f"User: {str(user_id)} tries to save {amount_to_buy}"
                          f" products: {str(product_id)} of shop_id: {str(shop_id)}")
        self.commerce_system_facade.save_product_to_cart(
            user_id, shop_id, product_id, amount_to_buy, purchase_type_id, **pt_args
        )
        event_logger.info(f"User: {user_id} successfully save the product {product_id}")
        return make_status_dict(True, "", "")

    @handler
    def change_product_purchase_type(self, user_id: int, shop_id: int, product_id: int, purchase_type_id: int,
                                     **pt_args):
        event_logger.info(f" User {user_id} tries to change {product_id} purchase type")
        res = self.commerce_system_facade.change_product_purchase_type(
            user_id, shop_id, product_id, purchase_type_id, pt_args
        )
        return make_status_dict(True, "", res)

    # 2.8
    @handler
    def get_cart_info(self, user_id: int) -> dict:
        event_logger.info(f"User: {str(user_id)} tries to get his cart info")
        ret = self.commerce_system_facade.get_cart_info(user_id)
        event_logger.info(f"User: {user_id} successfully got his cart")
        return make_status_dict(True, "", ret)

    # 2.8
    @handler
    def remove_product_from_cart(self, user_id: int, shop_id: int, product_id: int, amount: int) -> dict:
        event_logger.info(f"User: {str(user_id)} tries to remove {str(amount)} "
                          f"products: {str(product_id)} of shop_id: {str(shop_id)}")
        self.commerce_system_facade.remove_product_from_cart(user_id, shop_id, product_id, amount)
        event_logger.info(f"User: {user_id} successfully save the product {product_id}")
        return make_status_dict(True, "", "")

    # 2.9
    @handler
    def purchase_product(self, user_id: int, shop_id: int, product_id: int,
                         amount_to_buy: int, payment_details: dict, delivery_details: dict) -> dict:
        event_logger.info(f"User: {str(user_id)} tries to purchase {str(amount_to_buy)}"
                          f" products: {str(product_id)} of shop_id: {str(shop_id)}")
        self.commerce_system_facade.purchase_product(
            user_id, shop_id, product_id, amount_to_buy, payment_details, delivery_details
        )
        event_logger.info(f"User: {str(user_id)} successfully purchased the product {str(product_id)}")
        return make_status_dict(True, "", "")

    # 2.9
    @handler
    def purchase_shopping_bag(self, user_id: int, shop_id: int, payment_details: dict, delivery_details: dict) -> dict:
        event_logger.info(f"User: {str(user_id)} tries to purchase {str(shop_id)} bag")
        self.commerce_system_facade.purchase_shopping_bag(user_id, shop_id, payment_details, delivery_details)
        event_logger.info(f"User: {user_id} successfully purchased the bag of the shop {str(shop_id)}")
        return make_status_dict(True, "", "")

    # 2.9
    @handler
    def purchase_cart(self, user_id: int, payment_details: dict, delivery_details: dict,
                      all_or_nothing: bool = False) -> dict:
        event_logger.info(f"User: {str(user_id)} tries to purchase his cart")
        self.commerce_system_facade.purchase_cart(user_id, payment_details, delivery_details, all_or_nothing)
        event_logger.info(f"User: {user_id} successfully purchased his cart")
        return make_status_dict(True, "", "")

    # 3. Subscriber Requirements

    # 3.1
    @handler
    def logout(self, user_id: int) -> dict:
        self.commerce_system_facade.logout(user_id)
        event_logger.info(f"User: {user_id} Logged Out Successfully")
        return make_status_dict(True, "", "")

    # 3.2
    @handler
    def open_shop(self, user_id: int, **shop_details) -> dict:
        event_logger.info(f"User: {user_id} tries to open shop: {shop_details['shop_name']}")
        shop_id = self.commerce_system_facade.open_shop(user_id, **shop_details)
        event_logger.info(f"User: {user_id} opened shop: {shop_id} successfully")
        return make_status_dict(True, "", shop_id)

    # 3.7
    @handler
    def get_personal_purchase_history(self, user_id: int) -> dict:
        event_logger.info(f"User: {user_id} tries to get_personal_purchase_history")
        history = self.commerce_system_facade.get_personal_purchase_history(user_id)
        event_logger.info(f"User: {user_id} got personal purchase history successfully")
        return make_status_dict(True, "", history)

    # 4. Shop Owner Requirements

    # 4.1
    @handler
    def add_product_to_shop(self, user_id: int, shop_id: int, **product_info) -> dict:
        event_logger.info(f"User: {user_id} tries to add product to shop {shop_id}")
        pid = self.commerce_system_facade.add_product_to_shop(user_id, shop_id, **product_info)
        event_logger.info(f"User: {user_id} added product successfully")
        return make_status_dict(True, "", pid)

    # 4.1
    @handler
    def edit_product_info(
            self, user_id: int, shop_id: int, product_id: int,
            product_name: str = None, description: str = None,
            price: float = None, quantity: int = None, categories: List[str] = None,
            purchase_types=None
    ) -> dict:
        event_logger.info(f"User: {user_id} tries to edit product info of "
                          f"shop_id: {shop_id} product_id: {product_id}")
        self.commerce_system_facade.edit_product_info(
            user_id, shop_id, product_id, product_name, description, price, quantity, categories, purchase_types
        )
        event_logger.info(f"User: {user_id} Edit product info successfully")
        return make_status_dict(True, "", "")

    # 4.1
    @handler
    def delete_product(self, user_id: int, shop_id: int, product_id: int) -> dict:
        event_logger.info(f"User: {user_id} tries to delete product of "
                          f"shop_id: {shop_id} product_id: {product_id}")
        self.commerce_system_facade.delete_product(user_id, shop_id, product_id)
        event_logger.info("User: " + str(user_id) + " Delete product info successfully")
        return make_status_dict(True, "", "")

    # 4.2
    @handler
    def get_purchase_conditions(self, user_id: int, shop_id: int) -> dict:
        event_logger.info(f"User: {user_id} tries to get the purchase policies of shop: {shop_id}")
        ret = self.commerce_system_facade.get_purchase_conditions(user_id, shop_id)
        event_logger.info(f"User: {user_id} got purcahse policies of shop: {shop_id} successfully")
        return make_status_dict(True, "", ret)

    # 4.2
    @handler
    def add_purchase_condition(self, user_id: int, shop_id: int, **condition_dict):
        event_logger.info(f"User: {user_id} tries to add purchase condition "
                          f"shop_id: {shop_id}")
        self.commerce_system_facade.add_purchase_condition(user_id, shop_id, **condition_dict)
        event_logger.info("User: " + str(user_id) + " added condition successfully")
        return make_status_dict(True, "", "")

    # 4.2
    @handler
    def remove_purchase_condition(self, user_id: int, shop_id: int, condition_id: int):
        event_logger.info(f"User: {user_id} tries to remove purchase condition "
                          f"{condition_id} from"
                          f"shop_id: {shop_id}")
        self.commerce_system_facade.remove_purchase_condition(user_id, shop_id, condition_id)
        event_logger.info("User: " + str(user_id) + " removed condition successfully")
        return make_status_dict(True, "", "")

    # 4.5
    @handler
    def appoint_shop_manager(self, user_id: int, shop_id: int, username: str, permissions: List[str]) -> dict:
        event_logger.info(f"User:  {user_id} tries to appoint manager: {username} to shop_id: {shop_id}")
        self.commerce_system_facade.appoint_shop_manager(user_id, shop_id, username, permissions)
        event_logger.info(f"User: {user_id} Appointed shop manager: {username} successfully")
        return make_status_dict(True, "", "")

    # 4.3
    @handler
    def appoint_shop_owner(self, user_id: int, shop_id: int, username: str) -> dict:
        event_logger.info(f"User: {user_id} tries to appoint owner: {username} to shop_id: {shop_id}")
        self.commerce_system_facade.appoint_shop_owner(user_id, shop_id, username)
        event_logger.info(f"User: {user_id} Appointed shop owner: {username} successfully")
        return make_status_dict(True, "", "")

    # 4.3
    @handler
    def promote_shop_owner(self, user_id: int, shop_id: int, username: str) -> dict:
        event_logger.info(f"User: {user_id} tries to promote owner: {username} of shop_id: {shop_id}")
        self.commerce_system_facade.promote_shop_owner(user_id, shop_id, username)
        event_logger.info(f"User: {user_id} promoted shop owner: {username} successfully")
        return make_status_dict(True, "", "")

    # 4.6
    @handler
    def edit_manager_permissions(self, user_id: int, shop_id: int, username: str, permissions: List[str]) -> dict:
        event_logger.info(f"User: {user_id} tries to edit manager "
                          f"permissions of: {username} in shop_id: {shop_id}")
        self.commerce_system_facade.edit_manager_permissions(user_id, shop_id, username, permissions)
        event_logger.info(f"User: {user_id} Edited manager: {username} permissions successfully")
        return make_status_dict(True, "", "")

    # 4.7
    @handler
    def un_appoint_manager(self, user_id: int, shop_id: int, username: str) -> dict:
        event_logger.info(f"User: {user_id} tries to un appoint manager: {username} of shop_id: {shop_id}")
        self.commerce_system_facade.unappoint_shop_manager(user_id, shop_id, username)
        event_logger.info(f"User: {user_id} Un appointed manager: {username} successfully")
        return make_status_dict(True, "", "")

    # 4.7
    @handler
    def un_appoint_shop_owner(self, user_id: int, shop_id: int, username: str) -> dict:
        event_logger.info(f"User: {user_id} tries to un appoint owner: {username} of shop_id: {shop_id}")
        self.commerce_system_facade.unappoint_shop_owner(user_id, shop_id, username)
        event_logger.info(f"User: {user_id} Un appointed owner: {username} successfully")
        return make_status_dict(True, "", "")

    # 4.9
    @handler
    def get_shop_staff_info(self, user_id: int, shop_id: int) -> dict:
        event_logger.info(f"user {user_id} requested for shop {shop_id} staff information")
        return make_status_dict(True, "", self.commerce_system_facade.get_shop_staff_info(user_id, shop_id))

    # 4.11
    @handler
    def get_shop_transaction_history(self, user_id: int, shop_id: int) -> dict:
        event_logger.info(f"user {user_id} requested for shop {shop_id} transaction history")
        return make_status_dict(True, "",
                                self.commerce_system_facade.get_shop_transaction_history(user_id, shop_id))

    # 6. System Administrator Requirements

    # 6.4
    @handler
    def get_system_transactions(self, user_id: int):
        event_logger.info(f"user {user_id} requested for the system transaction history")
        return make_status_dict(True, "", self.commerce_system_facade.get_system_transaction_history(user_id))

    @handler
    def get_product_info(self, user_id: int, shop_id: int, product_id: int) -> dict:
        event_logger.info(f"user {user_id} requested for product {product_id} info page")
        return make_status_dict(True, "", self.commerce_system_facade.get_product_info(shop_id, product_id))

    @handler
    def get_permissions(self, user_id: int, shop_id: int) -> dict:  # [permission: str, bool]
        return make_status_dict(True, "", self.commerce_system_facade.get_permissions(user_id, shop_id))

    @handler
    def get_discounts(self, user_id: int, shop_id: int) -> dict:
        event_logger.info(f"User: {user_id} tries to get the discounts of shop: {shop_id}")
        ret = self.commerce_system_facade.get_discounts(user_id, shop_id)
        event_logger.info(f"User: {user_id} got discounts of shop: {shop_id} successfully")
        return make_status_dict(True, "", ret)

    @handler
    def add_discount(self, user_id: int, shop_id: int, has_cond: bool, condition: List[Union[str, SimpleCond, List]],
                     discount: Union[DiscountDict, CompositeDiscountDict]) -> dict:
        event_logger.info(f"User: {user_id} tries to add discount to shop: {shop_id}")
        discount_id = self.commerce_system_facade.add_discount(user_id, shop_id, has_cond, condition, discount)
        event_logger.info(f"User: {user_id} added discount to shop: {shop_id} successfully")
        return make_status_dict(True, "", discount_id)

    @handler
    def aggregate_discounts(self, user_id: int, shop_id: int, discount_ids: List[int], operator: str):
        event_logger.info(f"User: {user_id} tries to aggregate discounts to shop: {shop_id}")
        self.commerce_system_facade.aggregate_discounts(user_id, shop_id, discount_ids, operator)
        event_logger.info(f"User: {user_id} aggregated discounts to shop: {shop_id} successfully")
        return make_status_dict(True, "", "")

    @handler
    def move_discount_to(self, user_id: int, shop_id: int, src_discount_id: int, dst_discount_id: int):
        event_logger.info(f"User: {user_id} tries to move discounts in shop: {shop_id}")
        self.commerce_system_facade.move_discount_to(user_id, shop_id, src_discount_id, dst_discount_id)
        event_logger.info(f"User: {user_id} moved discounts in shop: {shop_id} successfully")
        return make_status_dict(True, "", "")

    @handler
    def delete_discounts(self, user_id: int, shop_id, discount_ids: List[int]):
        event_logger.info(f"User: {user_id} tries to delete discounts to shop: {shop_id}")
        self.commerce_system_facade.delete_discounts(user_id, shop_id, discount_ids)
        event_logger.info(f"User: {user_id} deleted discounts to shop: {shop_id} successfully")
        return make_status_dict(True, "", "")

    @handler
    def get_user_appointemnts(self, user_id: int):
        event_logger.info(f"User: {user_id} tries to get his appointments")
        res = self.commerce_system_facade.get_user_appointments(user_id)
        event_logger.info(f"User: {user_id} got his appointments successfully")
        return make_status_dict(True, "", res)

    @handler
    def add_purchase_type(self, user_id: int, shop_id: int, product_id: int, **purchase_type_info: PurchaseTypeDict):
        event_logger.info(f"User: {user_id} tries to add a purchase type")
        res = self.commerce_system_facade.add_purchase_type(user_id, shop_id, product_id, purchase_type_info)
        event_logger.info(f"User: {user_id} added a purchase type successfully")
        return make_status_dict(True, "", res)

    @handler
    def offer_price(self, user_id: int, shop_id: int, product_id: int, offer: float):
        event_logger.info(f"User: {user_id} tries to offer {offer} for product {product_id}")
        res = self.commerce_system_facade.offer_price(user_id, shop_id, product_id, offer)
        event_logger.info(f"User: {user_id} succefully offered")
        return make_status_dict(True, "", res)

    @handler
    def reply_price_offer(self, user_id: int, shop_id: int, product_id: int, offer_maker: str, action: str):
        event_logger.info(f"User: {user_id} tries to reply to offer for product {product_id}")
        res = self.commerce_system_facade.reply_price_offer(user_id, shop_id, product_id, offer_maker, action)
        event_logger.info(f"User: {user_id} replied successfully")
        return make_status_dict(True, "", res)

    def cleanup(self):
        self.commerce_system_facade.clean_up()
