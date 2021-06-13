import threading
from typing import Dict
import domain.commerce_system.valdiation as validate

import hashlib
import os

from config.config import config, ConfigFields as cf


def encrypt_password(plaintext_password: str, salt=None) -> Dict:
    if not salt:
        if not salt:
        salt = os.urandom(32)  # A new salt for this user
    if config[cf.HASH_ALG] == "modulo":
        key = int.from_bytes(plaintext_password.encode() + salt, 'big', signed=False) % int(1E10)
    else:

    key = int.from_bytes(plaintext_password.encode() + salt, 'big', signed=False) % int(1E10)

    # key = hashlib.pbkdf2_hmac(config[cf.HASH_ALG], plaintext_password.encode('utf-8'), salt, 100000)
    return {'salt': salt, 'key': key}


class Authenticator:
    users_passwords_lock = threading.Lock()

    def __init__(self):
        self.users_passwords: Dict[str, Dict] = {}  # [username, password (encrypted)]

    def register_new_user(self, username: str, plaintext_password: str):
        with self.users_passwords_lock:
            assert username not in self.users_passwords, "Username already exists"
            assert validate.validate_username(username), "Username length needs to be between 1 - 20 characters"
            assert validate.validate_password(plaintext_password), \
                "Password length needs to be between 6 - 20 characters"

            encrypted_password = encrypt_password(plaintext_password)
            self.users_passwords[username] = encrypted_password

    # receives plaintext password, returns dictionary of salt, encrypted password

    def login(self, username: str, plaintext_password: str):
        with self.users_passwords_lock:
            assert username in self.users_passwords, "Username doesn't exists"

            salt = self.users_passwords[username]['salt']  # Get the salt
            key = self.users_passwords[username]['key']  # Get the correct key
            new_key = encrypt_password(plaintext_password, salt=salt)["key"]
            assert key == new_key, "Wrong password"
