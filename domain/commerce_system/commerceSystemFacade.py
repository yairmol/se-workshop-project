import threading
from typing import Dict

from domain.commerce_system.facade import ICommerceSystemFacade
from domain.commerce_system.user import User, Subscribed
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

    def register(self, user_id: int, username: str, password: str, **more) -> bool:
        assert not self.is_username_exists(username), "Username already exists"
        assert validate.validate_username(username), "Username length needs to be between 0 - 20 characters"
        assert validate.validate_password(password), "Password length needs to be between 0 - 20 characters"

        new_subscribe = Subscribed(username)
        # saving registered user's details
        self.registered_users_lock.acquire()
        self.registered_users[username] = new_subscribe
        self.registered_users_lock.release()

    def is_username_exists(self, username: str):
        self.registered_users_lock.acquire()
        ret_val = username in self.registered_users
        self.registered_users_lock.release()
        return ret_val

    def login(self, session_id: int, username: str, password: str) -> bool:
        pass

    def logout(self, session_id: int) -> bool:
        pass
