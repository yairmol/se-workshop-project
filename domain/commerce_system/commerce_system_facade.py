import threading
from typing import Dict, List

from domain.commerce_system.ifacade import ICommerceSystemFacade
from domain.commerce_system.product import Product
from domain.commerce_system.search_engine import search, Filter
from domain.commerce_system.user import User, Subscribed, Guest
import domain.commerce_system.valdiation as validate


class CommerceSystemFacade(ICommerceSystemFacade):

    active_users_lock = threading.Lock()
    registered_users_lock = threading.Lock()

    def __init__(self):
        self.active_users: Dict[int, User] = {}  # dictionary {user.id : user object}
        self.registered_users: Dict[str, Subscribed] = {}  # dictionary {user.username : user object}

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

    def _get_all_products(self) -> List[Product]:
        # TODO: implement when there will be a list of shops in the facade
        raise NotImplementedError()

    def search_products(
            self, product_name: str = None, keywords: List[str] = None,
            categories: List[str] = None, filters: List[dict] = None
    ) -> List[dict]:
        products: List[Product] = self._get_all_products()
        search_results = search(
            products, product_name, keywords, categories, list(map(Filter.from_dict, filters))
        )
        return list(map(lambda p: {
            "product_name": p.name,
            "price": p.price,
            "description": p.description,
            "quantity": p.quantity,
            "categories": p.categories
        }, search_results))
