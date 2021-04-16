import threading
from typing import Dict, List

from domain.commerce_system.facade import ICommerceSystemFacade
from domain.commerce_system.user import User, Subscribed, Guest
import domain.commerce_system.valdiation as validate


class CommerceSystemFacade(ICommerceSystemFacade):
    def exit(self, session_id: int) -> bool:
        pass

    def get_shop_info(self, shop_id: str) -> dict:
        pass

    def save_product_to_cart(self, session_id: int, shop_id: str, product_id: str) -> bool:
        pass

    def get_cart_info(self, session_id: int) -> dict:
        pass

    def search_products(self, keywords: str, filters: list) -> List[dict]:
        pass

    def search_shops(self, keywords: str, filters: list) -> List[dict]:
        pass

    def purchase_cart(self, session_id: int) -> dict:
        pass

    def purchase_product(self, session_id: int, shop_id: str, product_id: str) -> dict:
        pass

    def open_shop(self, session_id: int, **shop_details) -> int:
        pass

    def get_personal_purchase_history(self, session_id: int) -> List[dict]:
        pass

    def add_product_to_shop(self, session_id: int, shop_id: str, **product_info) -> int:
        pass

    def edit_product_info(self, session_id: int, shop_id: str, **product_info) -> bool:
        pass

    def delete_product(self, session_id: int, shop_id: str, product_id: str) -> bool:
        pass

    def appoint_shop_owner(self, session_id: int, shop_id: str, username: str) -> bool:
        pass

    def appoint_shop_manager(self, session_id: int, shop_id: str, username: str, permissions: List[str]) -> bool:
        pass

    def edit_manager_permissions(self, session_id: int, shop_id: str, username: str, permissions: dict) -> bool:
        pass

    def unappoint_shop_worker(self, session_id: int, shop_id: str, username: str) -> bool:
        pass

    def get_shop_staff_info(self, session_id: int, shop_id: str) -> List[dict]:
        pass

    def get_shop_transaction_history(self, session_id: int, shop_id: str) -> List[dict]:
        pass

    def get_system_transaction_history(self, session_id: int) -> List[dict]:
        pass

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
