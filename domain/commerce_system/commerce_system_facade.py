import threading
from typing import Dict, List, Union, Optional

from config.config import config, ConfigFields as cf
from data_model import ConditionsModel as Cm
from domain.authentication_module.authenticator import Authenticator
from domain.commerce_system.ifacade import ICommerceSystemFacade
from domain.commerce_system.product import Product
from domain.commerce_system.purchase_conditions import (
    TimeWindowForCategoryCondition, MaxQuantityForProductCondition, ORCondition, ANDCondition,
    DateWindowForProductCondition, TimeWindowForProductCondition, DateWindowForCategoryCondition,
)
from domain.commerce_system.search_engine import search, Filter
from domain.commerce_system.shop import Shop
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.transaction_repo import TransactionRepo
from domain.commerce_system.user import User, Subscribed, SystemManager
from domain.discount_module.discount_management import SimpleCond, DiscountDict, CompositeDiscountDict
from domain.notifications.notifications import INotifications

condition_map = {
    Cm.MAX_QUANTITY_FOR_PRODUCT: MaxQuantityForProductCondition,
    Cm.TIME_WINDOW_FOR_CATEGORY: TimeWindowForCategoryCondition,
    Cm.TIME_WINDOW_FOR_PRODUCT: TimeWindowForProductCondition,
    Cm.DATE_WINDOW_FOR_CATEGORY: DateWindowForCategoryCondition,
    Cm.DATE_WINDOW_FOR_PRODUCT: DateWindowForProductCondition,
    Cm.AND: ANDCondition,
    Cm.OR: ORCondition
}


class CommerceSystemFacade(ICommerceSystemFacade):
    active_users_lock = threading.Lock()
    registered_users_lock = threading.Lock()
    shops_lock = threading.Lock()

    def __init__(self, authenticator: Authenticator, notifications: INotifications):
        self.active_users: Dict[int, User] = {}  # dictionary {user_sess.id : user_sess object}
        self.registered_users: Dict[str, Subscribed] = {}  # dictionary {user_id.username : user_sess object}
        self.shops: Dict[int, Shop] = {}  # dictionary {shop.shop_id : shop}
        self.transaction_repo = TransactionRepo.get_transaction_repo()
        self.authenticator = authenticator
        self.notifications = notifications

    # 2.1
    def enter(self) -> int:
        new_user = User()
        with self.active_users_lock:
            self.active_users[new_user.id] = new_user

        return new_user.id

    # 2.2
    def exit(self, session_id: int) -> bool:
        pass

    # 2.3
    def register(self, user_id: int, username: str, password: str, **more) -> bool:
        self.authenticator.register_new_user(username, password)
        user = self.get_user(user_id)
        new_subscribe = user.register(username)
        # saving registered user_sess's details
        with self.registered_users_lock:
            self.registered_users[username] = new_subscribe
        return True

    # 2.4
    def login(self, user_id: int, username: str, password: str) -> bool:
        self.authenticator.login(username, password)
        with self.registered_users_lock:
            sub_user = self.registered_users.get(username)

        # **************** NEED TO CHECK IF THE USER IS GUEST ?
        with self.active_users_lock:
            self.active_users.get(user_id).login(sub_user)
        return True

    def get_user_info(self, user_id: int) -> dict:
        return self.active_users[user_id].to_dict()

    # 2.5
    def get_shop_info(self, shop_id: int) -> dict:
        shop: Shop = self.shops[shop_id]
        return shop.to_dict()

    def get_all_shop_info(self) -> List[dict]:
        shops = [shop.to_dict() for shop in self.shops.values()]
        return shops

    def get_all_shop_ids_and_names(self) -> Dict[int, str]:
        ret = {}
        for shopId in self.shops.keys():
            ret[shopId] = self.shops[shopId].name
        return ret

    def get_all_user_names(self) -> List[str]:
        names: List[str] = list(self.registered_users.keys())
        return names

    def get_all_categories(self) -> List[str]:
        cats = set()
        for shop in self.shops.values():
            for prod in shop.products.values():
                cats.update(prod.get_category_names())
        return list(cats)

    # 2.6
    def search_products(
            self, product_name: str = None, keywords: List[str] = None,
            categories: List[str] = None, filters: List[dict] = None
    ) -> List[dict]:
        if not filters:
            filters = []
        if not keywords:
            keywords = []
        if not categories:
            categories = []
        if not product_name:
            product_name = ""
        products: List[Product] = self._get_all_products()
        search_results = search(
            products, product_name, keywords, categories, list(map(Filter.from_dict, filters))
        )
        return list(map(lambda p: p.to_dict(), search_results))

    # 2.7, 2.8
    def save_product_to_cart(self, user_id: int, shop_id: int, product_id: int, amount_to_buy: int) -> bool:
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        product = shop.products[product_id]
        return user.save_product_to_cart(shop, product, amount_to_buy)

    # 2.8
    def remove_product_from_cart(self, user_id: int, shop_id: int, product_id: int, amount: int) -> bool:
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        product = shop.products[product_id]
        return user.remove_product_from_cart(shop, product, amount)

    # 2.8
    def get_cart_info(self, user_id: int) -> dict:
        user = self.get_user(user_id)
        return user.get_cart_info()

    # 2.9
    def purchase_cart(self, user_id: int, payment_details: dict, delivery_details: dict,
                      do_what_you_can=False) -> List[dict]:
        user = self.get_user(user_id)
        return [t.to_dict() for t in user.purchase_cart(payment_details, delivery_details, do_what_you_can)]

    # 2.9
    def purchase_shopping_bag(self, user_id: int, shop_id: int, payment_details: dict,
                              delivery_details: dict) -> dict:
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        return user.purchase_shopping_bag(shop, payment_details, delivery_details).to_dict()

    # 2.9
    def purchase_product(self, user_id: int, shop_id: int, product_id: int, amount_to_buy: int,
                         payment_details: dict, delivery_details: dict) -> dict:
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        product = shop.products[product_id]
        return user.purchase_product(shop, product, amount_to_buy, payment_details, delivery_details).to_dict()

    # 3.1
    def logout(self, user_id: int) -> bool:
        with self.active_users_lock:
            return self.active_users.get(user_id).logout()

    # 3.2
    def open_shop(self, user_id: int, **shop_details) -> int:
        worker = self.get_user(user_id).user_state
        assert len([s for s in self.shops.values() if s.name == shop_details["shop_name"]]) == 0
        new_shop = worker.open_shop(shop_details)
        self.add_shop(new_shop)
        return new_shop.shop_id

    # 3.7
    def get_personal_purchase_history(self, user_id: int) -> List[dict]:
        transactions: List[Transaction] = self.get_user(user_id).get_personal_transactions_history()
        return [t.to_dict() for t in transactions]

    # 4.1
    def add_product_to_shop(self, user_id: int, shop_id: int, **product_info) -> int:
        shop = self.get_shop(shop_id)
        worker = self.get_user(user_id).user_state
        return worker.add_product(shop, **product_info).product_id

    # 4.1
    def edit_product_info(
            self, user_id: int, shop_id: int, product_id: int,
            product_name: str, description: str, price: float,
            quantity: int, categories: List[str]
    ) -> bool:
        shop = self.get_shop(shop_id)
        worker = self.get_user(user_id).user_state
        to_edit = {key: value for key, value in [
            ("product_name", product_name), ("description", description),
            ("price", price), ("quantity", quantity), ("categories", categories),
        ] if value is not None}
        return worker.edit_product(shop, product_id, **to_edit)

    # 4.1
    def delete_product(self, user_id: int, shop_id: int, product_id: int) -> bool:
        shop = self.get_shop(shop_id)
        worker = self.get_user(user_id).user_state
        return worker.delete_product(shop, product_id)

    # 4.2
    def get_purchase_conditions(self, user_id: int, shop_id: int) -> List[dict]:
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        return list(map(lambda d: d.to_dict(), user.get_shop_purchase_conditions(shop)))

    # 4.2
    def get_discounts(self, user_id, shop_id) -> List[dict]:
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        return [d.to_dict() for d in user.get_shop_discounts(shop)]

    # 4.2
    def add_discount(
            self, user_id: int, shop_id: int, has_cond: bool, condition: Optional[List[Union[str, SimpleCond, List]]],
            discount: Union[DiscountDict, CompositeDiscountDict]
    ) -> int:

        shop = self.get_shop(shop_id)
        subscribed = self.get_user(user_id).user_state
        return subscribed.add_discount(shop, has_cond, condition, discount).discount_id

    # 4.2
    def delete_discounts(self, user_id: int, shop_id, discount_ids) -> bool:
        shop = self.get_shop(shop_id)
        subscribed = self.get_user(user_id).user_state
        return subscribed.delete_discounts(shop, discount_ids)

    # 4.2
    def aggregate_discounts(self, user_id: int, shop_id: int, discount_ids: [int], func: str) -> bool:
        shop = self.get_shop(shop_id)
        subscribed = self.get_user(user_id).user_state
        return subscribed.aggregate_discounts(shop, discount_ids, func)

    # 4.2
    def move_discount_to(self, user_id: int, shop_id: int, src_discount_id: int, dst_discount_id: int) -> bool:
        shop = self.get_shop(shop_id)
        subscribed = self.get_user(user_id).user_state
        return subscribed.move_discount_to(shop, src_discount_id, dst_discount_id)

    # 4.2
    def add_purchase_condition(self, user_id: int, shop_id: int, **condition_dict) -> bool:
        worker = self.get_user(user_id).user_state
        shop = self.get_shop(shop_id)
        if condition_dict[Cm.CONDITION_TYPE] == Cm.AND or condition_dict[Cm.CONDITION_TYPE] == Cm.OR:
            conditions = []
            for cond_dict in condition_dict[Cm.CONDITIONS]:
                conditions += [condition_map[cond_dict[Cm.CONDITION_TYPE]](cond_dict)]
            condition_dict[Cm.CONDITIONS] = conditions
        condition = condition_map[condition_dict[Cm.CONDITION_TYPE]](condition_dict)
        return worker.add_purchase_condition(shop, condition)

    # 4.2
    def remove_purchase_condition(self, user_id: int, shop_id: int, condition_id: int) -> bool:
        worker = self.get_user(user_id).user_state
        shop = self.get_shop(shop_id)
        return worker.remove_purchase_condition(shop, condition_id)

    # 4.3
    def appoint_shop_owner(self, user_id: int, shop_id: int, username: str) -> dict:
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id)
        new_owner = self.get_subscribed(username)
        app = owner.user_state.appoint_owner(new_owner, shop)
        # TODO: change or delete value of userid here and below
        new_owner.send_message(f"{owner.get_name()} appointed you as owner to {shop.name}")
        return app.to_dict()

    # 4.5
    def appoint_shop_manager(self, user_id: int, shop_id: int, username: str, permissions: List[str]) -> dict:
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id)
        new_manager = self.get_subscribed(username)
        app = owner.user_state.appoint_manager(new_manager, shop, permissions)
        new_manager.send_message(f"{owner.get_name()} appointed you as owner to {shop.name}")
        return app.to_dict()

    # 4.6
    def edit_manager_permissions(self, user_id: int, shop_id: int, username: str, permissions: List[str]) -> bool:
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id)
        new_owner = self.get_subscribed(username)
        res = owner.user_state.edit_manager_permissions(new_owner, shop, permissions)
        new_owner.send_message(f"{owner.get_name()} edited your permissions in shop {shop.name}")
        return res

    # 4.3
    def promote_shop_owner(self, user_id: int, shop_id: int, username: str) -> dict:
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id)
        new_owner = self.get_subscribed(username)
        app = owner.user_state.promote_manager_to_owner(new_owner, shop)
        new_owner.send_message(f"{owner.get_name()} promoted you to owner in {shop.name}")
        return app.to_dict()

    def unappoint_shop_manager(self, user_id: int, shop_id: int, username: str) -> bool:
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id)
        old_owner = self.get_subscribed(username)
        res = owner.user_state.un_appoint_manager(old_owner, shop)
        old_owner.send_message(f"{owner.get_name()} unappointed you as manager in {shop.name}")
        return res

    # 4.7
    def unappoint_shop_owner(self, user_id: int, shop_id: int, username: str) -> bool:
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id)
        old_owner = self.get_subscribed(username)
        res = owner.user_state.un_appoint_owner(old_owner, shop)
        old_owner.send_message(f"{owner.get_name()} unappointed you as owner in {shop.name}")
        return res

    # 4.9
    def get_shop_staff_info(self, user_id: int, shop_id: int) -> List[dict]:
        return [a.to_dict() for a in self.get_user(user_id).get_shop_staff_info(self.get_shop(shop_id))]

    # 4.11
    def get_shop_transaction_history(self, user_id: int, shop_id: int) -> List[dict]:
        shop = self.get_shop(shop_id)
        user = self.get_user(user_id)
        return [t.to_dict() for t in user.user_state.get_shop_transaction_history(shop)]

    # 6.4
    def get_system_transaction_history(self, user_id: int) -> List[dict]:
        user = self.get_user(user_id)
        transactions = user.user_state.get_system_transaction_history()
        return list(map(lambda t: t.to_dict(), transactions))

    # 6.4
    def get_system_transaction_history_of_shop(self, user_id: int, shop_id: int) -> List[dict]:
        user = self.get_user(user_id)
        transactions = user.user_state.get_system_transaction_history_of_shop(shop_id)
        return [t.to_dict() for t in transactions]

    # 6.4
    def get_system_transaction_history_of_user(self, user_id: int, username: str) -> List[dict]:
        user = self.get_user(user_id)
        transactions = user.user_state.get_system_transaction_history_of_user(username)
        return list(map(lambda t: t.to_dict(), transactions))

    # utils:
    def remove_active_user(self, user_id: int) -> None:
        with self.active_users_lock:
            self.active_users.pop(user_id)

    def is_username_exists(self, username: str) -> bool:
        with self.registered_users_lock:
            return username in self.registered_users

    def get_user(self, user_id) -> User:
        with self.active_users_lock:
            ret = self.active_users[user_id]

        return ret

    def get_subscribed(self, username) -> Subscribed:
        with self.registered_users_lock:
            return self.registered_users[username]

    def get_shop(self, shop_id) -> Shop:
        with self.shops_lock:
            return self.shops[shop_id]

    def add_shop(self, shop):
        with self.shops_lock:
            self.shops[shop.shop_id] = shop

    def _get_all_products(self) -> List[Product]:
        products = []
        for shop in self.shops.values():
            products.extend(shop.products.values())
        return products

    def create_admin_user(self):
        admin_un = config[cf.ADMIN_CREDENTIALS][cf.ADMIN_USERNAME]
        admin_password = config[cf.ADMIN_CREDENTIALS][cf.ADMIN_PASSWORD]
        self.authenticator.register_new_user(admin_un, admin_password)
        self.registered_users[admin_un] = SystemManager(
            admin_password, self.transaction_repo
        )

    def get_product_info(self, shop_id, product_id):
        return self.shops.get(shop_id).get_product_info(product_id).to_dict()

    def get_permissions(self, user_id, shop_id) -> dict:
        shop = self.get_shop(shop_id)
        subscribed = self.get_user(user_id).user_state
        ret = subscribed.get_permissions(shop)
        return ret

    def get_user_appointments(self, user_id):
        user = self.get_user(user_id)
        return [a.to_dict() for a in user.user_state.get_appointments()]

    def clean_up(self):
        self.transaction_repo = self.transaction_repo.cleanup()
        self.shops.clear()
        self.registered_users.clear()
        self.active_users.clear()
