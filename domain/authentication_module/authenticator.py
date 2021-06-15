import threading
from typing import Dict
import domain.commerce_system.valdiation as validate

import hashlib
import os

from config.config import config, ConfigFields as cf
from data_access_layer.engine import get_first, save


class Password:
    def __init__(self, username, password_hash, salt):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt


def encrypt_password(plaintext_password: str, username, salt=None) -> Password:
    if not salt:
        salt = os.urandom(32)  # A new salt for this user
    if config[cf.HASH_ALG] == "modulo":
        key = int.from_bytes(plaintext_password.encode() + salt, 'big', signed=False) % int(1E10)
    else:
        key = hashlib.pbkdf2_hmac(config[cf.HASH_ALG], plaintext_password.encode('utf-8'), salt, 100000)
    return Password(username, key, salt)


class Authenticator:
    users_passwords_lock = threading.Lock()

    def __init__(self):
        self._users_passwords: Dict[str, Dict] = {}  # [username, password (encrypted)]

    def users_passwords(self, username):
        if username not in self._users_passwords:
            # try:
            #     self._users_passwords[username] = get_first(Password, username=username)
            # except Exception as e:
            #     raise Exception("no password found")
            return None
        return self._users_passwords[username]

    def has_user(self, username):
        if username not in self._users_passwords:
            # try:
            #     p = get_first(Password, username=username)
            #     if p:
            #         self._users_passwords[username] = p
            #     return p
            # except Exception as e:
            return None
        return self._users_passwords[username]

    def register_new_user(self, username: str, plaintext_password: str):
        with self.users_passwords_lock:
            assert not self.has_user(username), "Username already exists"
            assert validate.validate_username(username), "Username length needs to be between 1 - 20 characters"
            assert validate.validate_password(plaintext_password), \
                "Password length needs to be between 6 - 20 characters"

            encrypted_password = encrypt_password(plaintext_password, username)
            self._users_passwords[username] = encrypted_password
            # save(encrypted_password)

    # receives plaintext password, returns dictionary of salt, encrypted password

    def login(self, username: str, plaintext_password: str):
        with self.users_passwords_lock:
            pass_obj = self.has_user(username)
            assert pass_obj, "Username doesn't exists"
            salt = pass_obj.salt  # Get the salt
            key = pass_obj.password_hash  # Get the correct key
            new_key = encrypt_password(plaintext_password, username, salt=salt).password_hash
            assert key == new_key, "Wrong password"
