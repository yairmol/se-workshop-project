# import threading
# from typing import Dict
#
# from domain.commerce_system.user import User
# import domain.commerce_system.valdiation as validate
# from domain.commerce_system.user import Subscribed, Guest
#
#
# class UserManagement:
#     active_users_lock = threading.Lock()
#     registered_users_lock = threading.Lock()
#
#     def __init__(self, authenticator):
#         self.active_users: Dict[int, User] = {}  # dictionary {user.id : user object}
#         self.registered_users = {}  # dictionary {user.username : user object}
#         self.authenticator = authenticator
#
#     def add_active_user(self) -> int:
#         new_user = User()
#         token = self.authenticator.add_new_user_token(new_user.id)
#         self.active_users_lock.acquire()
#         self.active_users[new_user.id] = new_user
#         self.active_users_lock.release()
#         return token
#
#     def remove_active_user(self, token: str) -> None:
#         self.active_users_lock.acquire()
#         user_id: int = self.authenticator.remove_token(token)
#         if user_id > 0:
#             if user_id in self.active_users:
#                 self.active_users.pop(user_id)
#             else:
#                 print("LOG: Error - User's Token exists, but user object is missing ")
#         else:
#             print("LOG: Error - User's Token doesn't exists")
#         self.active_users_lock.release()
#
#     def register(self, token, username: str, password: str) -> bool:
#         assert self.validate_token(token), "Token Expired"
#         assert not self.is_username_exists(username), "Username already exists"
#         assert validate.validate_username(username), "Username length needs to be between 0 - 20 characters"
#         assert validate.validate_password(password), "Password length needs to be between 0 - 20 characters"
#         user_id = self.authenticator.get_id_by_token(token)
#         new_subscribe = Subscribed(username)
#         # saving registered user's details
#         self.registered_users_lock.acquire()
#         self.registered_users[username] = new_subscribe
#         self.registered_users_lock.release()
#
#
#     def is_username_exists(self, username: str):
#         self.registered_users_lock.acquire()
#         ret_val = username in self.registered_users
#         self.registered_users_lock.release()
#         return ret_val
#
#     # checks if the token is expired (before executing a command)
#     # if the token is valid, extending it's expire time
#     def validate_token(self, token: str) -> bool:
#         if self.authenticator.is_token_expired(token):
#             return False
#         self.authenticator.extend_expire_time(token)
#         return True
