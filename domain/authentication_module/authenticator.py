import string
import threading
from typing import Dict
import domain.commerce_system.valdiation as validate

import hashlib
import os


def encrypt_password(plaintext_password: str) -> Dict:
    salt = os.urandom(32)  # A new salt for this user
    key = hashlib.pbkdf2_hmac('sha256', plaintext_password.encode('utf-8'), salt, 100000)
    return {'salt': salt, 'key': key}


class Authenticator:
    users_passwords_lock = threading.Lock()

    def __init__(self):
        self.users_passwords: Dict[str, Dict] = {}  # [username, password (encrypted)]

    def register_new_user(self, username: str, plaintext_password: str):
        self.users_passwords_lock.acquire()
        try:
            assert username not in self.users_passwords, "Username already exists"
            assert validate.validate_username(username), "Username length needs to be between 1 - 20 characters"
            assert validate.validate_password(plaintext_password), "Password length needs to be between 6 - 20 characters"
        except AssertionError as e:
            self.users_passwords_lock.release()
            raise e

        encrypted_password = encrypt_password(plaintext_password)
        self.users_passwords[username] = encrypted_password
        self.users_passwords_lock.release()

    # receives plaintext password, returns dictionary of salt, encrypted password

    def login(self, username: str, plaintext_password: str):
        self.users_passwords_lock.acquire()
        is_username_exists = username in self.users_passwords
        self.users_passwords_lock.release()
        if not is_username_exists:
            raise AssertionError("Username doesn't exists")

        self.users_passwords_lock.acquire()
        salt = self.users_passwords[username]['salt']  # Get the salt
        key = self.users_passwords[username]['key']  # Get the correct key
        new_key = hashlib.pbkdf2_hmac('sha256', plaintext_password.encode('utf-8'), salt, 100000)
        self.users_passwords_lock.release()
        assert key == new_key, "Wrong password"