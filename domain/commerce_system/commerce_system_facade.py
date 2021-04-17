import threading
from typing import Dict, List

from domain.commerce_system.ifacade import ICommerceSystemFacade
from domain.commerce_system.product import Product
from domain.commerce_system.search_engine import search, Filter
from domain.commerce_system.shop import Shop
from domain.commerce_system.user import User, Subscribed, Guest
import domain.commerce_system.valdiation as validate


class CommerceSystemFacade(ICommerceSystemFacade):

    def exit(self, session_id: int) -> bool:
        pass

    def get_shop_info(self, shop_id: int) -> dict:
        shop: Shop = self.shops[shop_id]
        return shop.to_dict()

    def save_product_to_cart(self, user_id: int, shop_id: str, product_id: int, amount_to_buy: int) -> bool:
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        product = shop.products[product_id]
        return user.save_product_to_cart(shop, product, amount_to_buy)

    def get_cart_info(self, user_id: int) -> dict:
        pass

    def search_shops(self, keywords: str, filters: list) -> List[dict]:
        pass

    def purchase_cart(self, user_id: int, payment_details: dict, all_or_nothing: bool) -> bool:
        user = self.get_user(user_id)
        return user.buy_cart(payment_details, all_or_nothing)

    def purchase_shopping_bag(self, user_id: int, shop_id: str, payment_details: dict) -> bool:
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        return user.buy_shopping_bag(shop, payment_details)

    def purchase_product(self, user_id: int, shop_id: str, product_id: int, amount_to_buy: int,
                         payment_details: dict) -> bool:
        user = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        product = shop.products[product_id]
        return user.buy_product(shop, product, amount_to_buy, payment_details)

    def open_shop(self, session_id: int, **shop_details) -> int:
        pass

    def get_personal_purchase_history(self, session_id: int) -> List[dict]:
        pass

    """NEEDS TO BE CHANGED - HANDLE TRANSPORTING PRODUCT DATA DIFFERENTLY"""

    def add_product_to_shop(self, user_id: int, shop_id: str, product: Product) -> int:
        shop = self.get_shop(shop_id)
        worker = self.get_user(user_id).user_state
        return worker.add_product(shop, product)

    def edit_product_info(self, user_id: int, shop_id: str, product_id: int, **product_info):
        shop = self.get_shop(shop_id)
        worker = self.get_user(user_id).user_state
        worker.edit_product_info(shop, product_id, **product_info)

    def delete_product(self, user_id: int, shop_id: str, product_id: str) -> bool:
        shop = self.get_shop(shop_id)
        worker = self.get_user(user_id).user_state
        worker.delete_product(shop, product_id)

    def appoint_shop_owner(self, user_id: int, shop_id: int, username: str):
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id).user_state.get_appointment(shop)
        new_owner = self.get_subscribed(username)
        new_owner.appoint_owner(owner, shop)

    def appoint_shop_manager(self, user_id: int, shop_id: int, username: str, permissions: List[str]):
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id).user_state.get_appointment(shop)
        new_owner = self.get_subscribed(username)
        new_owner.appoint_manager(owner, shop, permissions)

    def edit_manager_permissions(self, user_id: int, shop_id: int, username: str, permissions: List[str]):
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id).user_state.get_appointment(shop)
        new_owner = self.get_subscribed(username)
        new_owner.edit_manager_permissions(owner, shop, permissions)

    def unappoint_shop_worker(self, user_id: int, shop_id: int, username: str):
        pass

    def un_appoint_manager(self, user_id: int, shop_id: int, username: str):
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id).user_state.get_appointment(shop)
        new_owner = self.get_subscribed(username)
        new_owner.un_appoint_manager(owner, shop)

    def unappoint_shop_owner(self, user_id: int, shop_id: int, username: str):
        shop = self.get_shop(shop_id)
        owner = self.get_user(user_id).user_state.get_appointment(shop)
        new_owner = self.get_subscribed(username)
        new_owner.un_appoint_owner(owner, shop)

    def get_shop_staff_info(self, session_id: int, shop_id: str) -> List[dict]:
        pass

    def get_shop_transaction_history(self, session_id: int, shop_id: str) -> List[dict]:
        pass

    def get_system_transaction_history(self, session_id: int) -> List[dict]:
        pass

    active_users_lock = threading.Lock()
    registered_users_lock = threading.Lock()
    shops_lock = threading.Lock()

    def __init__(self):
        self.active_users: Dict[int, User] = {}  # dictionary {user.id : user object}
        self.registered_users: Dict[str, Subscribed] = {}  # dictionary {user.username : user object}
        self.shops: Dict[int, Shop] = {}  # dictionary {shop.shop_id : shop}

    def enter(self) -> int:
        new_user = User()
        self.active_users_lock.acquire()
        self.active_users[new_user.id] = new_user
        self.active_users_lock.release()
        return new_user.id

    def remove_active_user(self, user_id: int) -> None:
        self.active_users_lock.acquire()
        self.active_users.pop(user_id)
        self.active_users_lock.release()

    def register(self, user_id: int, username: str, password: str, **more):
        assert not self.is_username_exists(username), "Username already exists"
        assert validate.validate_username(username), "Username length needs to be between 0 - 20 characters"
        assert validate.validate_password(password), "Password length needs to be between 0 - 20 characters"

        new_subscribe = Subscribed(username, password)
        # saving registered user's details
        self.registered_users_lock.acquire()
        self.registered_users[username] = new_subscribe
        self.registered_users_lock.release()

    def is_username_exists(self, username: str):
        self.registered_users_lock.acquire()
        ret_val = username in self.registered_users
        self.registered_users_lock.release()
        return ret_val

    def login(self, user_id: int, username: str, password: str):
        assert self.is_username_exists(username), "Username doesn't exists"
        sub_user = self.registered_users.get(username)
        assert sub_user.password == password, "Wrong Password"
        self.active_users_lock.acquire()
        self.active_users.get(user_id).set_user_state(sub_user)
        self.active_users_lock.release()

    def logout(self, user_id: int):
        self.active_users_lock.acquire()
        self.active_users.get(user_id).set_user_state(Guest())
        self.active_users_lock.release()

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

    def _get_all_products(self) -> List[Product]:
        products = []
        for shop in self.shops.values():
            products.extend(shop.products.values())
        return products

    def search_products(
            self, product_name: str = None, keywords: List[str] = None,
            categories: List[str] = None, filters: List[dict] = None
    ) -> List[dict]:
        products: List[Product] = self._get_all_products()
        search_results = search(
            products, product_name, keywords, categories, list(map(Filter.from_dict, filters))
        )
        return list(map(lambda p: p.to_dict(), search_results))
