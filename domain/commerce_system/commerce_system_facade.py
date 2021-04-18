import threading
from typing import Dict, List

from domain.commerce_system.ifacade import ICommerceSystemFacade
from domain.commerce_system.product import Product
from domain.commerce_system.search_engine import search, Filter
from domain.commerce_system.shop import Shop
from domain.commerce_system.user import User, Subscribed
import domain.commerce_system.valdiation as validate


class CommerceSystemFacade(ICommerceSystemFacade):

    active_users_lock = threading.Lock()
    registered_users_lock = threading.Lock()
    shops_lock = threading.Lock()

    def __init__(self):
        self.active_users: Dict[int, User] = {}  # dictionary {user_sess.id : user_sess object}
        self.registered_users: Dict[str, Subscribed] = {}  # dictionary {user_id.username : user_sess object}
        self.shops: Dict[int, Shop] = {}  # dictionary {shop.shop_id : shop}

    # 2.1
    def enter(self) -> int:
        new_user = User()
        self.active_users_lock.acquire()
        self.active_users[new_user.id] = new_user
        self.active_users_lock.release()
        return new_user.id

    # 2.2
    def exit(self, session_id: int) -> bool:
        pass

    # 2.3
    def register(self, user_id: int, username: str, password: str, **more):
        assert not self.is_username_exists(username), "Username already exists"
        assert validate.validate_username(username), "Username length needs to be between 0 - 20 characters"
        assert validate.validate_password(password), "Password length needs to be between 0 - 20 characters"
        user = self.get_user(user_id)
        new_subscribe = user.register(username, password)
        # saving registered user_sess's details
        self.registered_users_lock.acquire()
        self.registered_users[username] = new_subscribe
        self.registered_users_lock.release()

    # 2.4
    def login(self, user_id: int, username: str, password: str):
        assert self.is_username_exists(username), "Username doesn't exists"
        sub_user = self.registered_users.get(username)
        assert sub_user.password == password, "Wrong Password"
        self.active_users_lock.acquire()
        try:
            self.active_users.get(user_id).login(sub_user)
        except Exception as e:
            self.active_users_lock.release()
            raise e
        self.active_users_lock.release()

    # 2.5
    def get_shop_info(self, shop_id: int) -> dict:
        shop: Shop = self.shops[shop_id]
        return shop.to_dict()

    # 2.6
    def search_products(
            self, product_name: str = None, keywords: List[str] = None,
            categories: List[str] = None, filters: List[dict] = None
    ) -> List[dict]:
        products: List[Product] = self._get_all_products()
        search_results = search(
            products, product_name, keywords, categories, list(map(Filter.from_dict, filters))
        )
        return list(map(lambda p: p.to_dict(), search_results))

    # 2.7, 2.8
    def save_product_to_cart(self, user_id: int, shop_id: int, product_id: int, amount_to_buy: int):
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        product = shop.products[product_id]
        assert user.save_product_to_cart(shop, product, amount_to_buy), "save product to cart failed"

    # 2.8
    def remove_product_from_cart(self, user_id: int, shop_id: int, product_id: int, amount: int):
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        product = shop.products[product_id]
        assert user.remove_product_from_cart(shop, product, amount), "remove product from cart failed"

    # 2.8
    def get_cart_info(self, user_id: int) -> dict:
        user = self.get_user(user_id)
        return user.get_cart_info()

    # 2.9
    def purchase_cart(self, user_id: int, payment_details: dict, all_or_nothing: bool):
        user = self.get_user(user_id)
        assert user.buy_cart(payment_details, all_or_nothing), "purchase cart failed"

    # 2.9
    def purchase_shopping_bag(self, user_id: int, shop_id: int, payment_details: dict):
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        assert user.buy_shopping_bag(shop, payment_details), "purchase bag failed"

    # 2.9
    def purchase_product(self, user_id: int, shop_id: int, product_id: int, amount_to_buy: int,
                         payment_details: dict):
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        product = shop.products[product_id]
        assert user.buy_product(shop, product, amount_to_buy, payment_details), "purchase product failed"

    # 3.1
    def logout(self, user_id: int):
        self.active_users_lock.acquire()
        try:
            self.active_users.get(user_id).logout()
        except Exception as e:
            self.active_users_lock.release()
            raise e
        self.active_users_lock.release()

    # 3.2
    def open_shop(self, user_id: int, **shop_details) -> int:
        worker = self.get_user(user_id).user_state
        assert len([s for s in self.shops.values() if s.name == shop_details["shop_name"]]) == 0
        new_shop = worker.open_shop(shop_details)
        self.add_shop(new_shop)
        return new_shop.shop_id

    # 3.7
    def get_personal_purchase_history(self, user_id: int) -> List[dict]:
        transactions = self.get_user(user_id).get_personal_transactions_history()
        return list(map(lambda t: t.to_dict(), transactions))

    # 4.1
    def add_product_to_shop(self, user_id: int, shop_id: int, **product_info) -> int:
        shop = self.get_shop(shop_id)
        worker = self.get_user(user_id).user_state
        return worker.add_product(shop, **product_info)

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

    # 4.3
    def appoint_shop_owner(self, user_id: int, shop_id: int, username: str):
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id).user_state
        new_owner = self.get_subscribed(username)
        owner.appoint_owner(new_owner, shop)

    # 4.5
    def appoint_shop_manager(self, user_id: int, shop_id: int, username: str, permissions: List[str]):
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id).user_state
        new_manager = self.get_subscribed(username)
        owner.appoint_manager(new_manager, shop, permissions)

    # 4.6
    def edit_manager_permissions(self, user_id: int, shop_id: int, username: str, permissions: List[str]):
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id).user_state
        new_owner = self.get_subscribed(username)
        owner.edit_manager_permissions(new_owner, shop, permissions)

    # 4.3
    def promote_shop_owner(self, user_id: int, shop_id: int, username: str):
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id).user_state
        new_owner = self.get_subscribed(username)
        owner.promote_manager_to_owner(new_owner, shop)

    def unappoint_shop_manager(self, user_id: int, shop_id: int, username: str):
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id).user_state
        old_owner = self.get_subscribed(username)
        owner.un_appoint_manager(old_owner, shop)

    # 4.7
    def unappoint_shop_owner(self, user_id: int, shop_id: int, username: str):
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id).user_state
        old_owner = self.get_subscribed(username)
        owner.un_appoint_owner(old_owner, shop)

    # 4.9
    def get_shop_staff_info(self, user_id: int, shop_id: int) -> List[dict]:
        return self.get_shop(shop_id).get_staff_info()

    # 4.11
    def get_shop_transaction_history(self, user_id: int, shop_id: int) -> List[dict]:
        shop = self.get_shop(shop_id)
        user = self.get_user(user_id)
        return user.user_state.get_shop_transaction_history(shop)

    # 6.4
    def get_system_transaction_history(self, session_id: int) -> List[dict]:
        pass

    # utils:
    def remove_active_user(self, user_id: int) -> None:
        self.active_users_lock.acquire()
        self.active_users.pop(user_id)
        self.active_users_lock.release()

    def is_username_exists(self, username: str):
        self.registered_users_lock.acquire()
        ret_val = username in self.registered_users
        self.registered_users_lock.release()
        return ret_val

    def get_user(self, user_id) -> User:
        self.active_users_lock.acquire()
        ret = self.active_users[user_id]
        self.active_users_lock.release()
        return ret

    def get_subscribed(self, username) -> Subscribed:
        self.registered_users_lock.acquire()
        ret = self.registered_users[username]
        self.registered_users_lock.release()
        return ret

    def get_shop(self, shop_id) -> Shop:
        self.shops_lock.acquire()
        ret = self.shops[shop_id]
        self.shops_lock.release()
        return ret

    def add_shop(self, shop):
        self.shops_lock.acquire()
        self.shops[shop.shop_id] = shop
        self.shops_lock.release()

    def _get_all_products(self) -> List[Product]:
        products = []
        for shop in self.shops.values():
            products.extend(shop.products.values())
        return products
