import datetime
import secrets
import string
import threading
import time


class Authenticator:
    alphabet = string.ascii_letters + string.digits
    tokens_ids_lock = threading.Lock()
    tokens_time_lock = threading.Lock()
    session_time = 1  # hours

    def __init__(self):
        self.tokens_ids = {}
        self.tokens_expire_time = {}

    def is_token_exists(self, token: str) -> bool:
        self.tokens_ids_lock.acquire()
        ret_val = token in self.tokens_ids
        self.tokens_ids_lock.release()
        return ret_val

    def generate_token(self) -> str:
        new_token = ''.join(secrets.choice(self.alphabet) for i in range(8))
        while new_token in self.tokens_ids:
            new_token = ''.join(secrets.choice(self.alphabet) for i in range(8))
        return new_token

    def add_new_user_token(self, user_id: int) -> str:
        self.tokens_ids_lock.acquire()
        new_token = self.generate_token()
        self.tokens_ids[new_token] = user_id

        current_date_and_time = datetime.datetime.now()
        hours_added = datetime.timedelta(hours=self.session_time)
        expire_date = current_date_and_time + hours_added
        self.tokens_time_lock.acquire()
        self.tokens_expire_time[new_token] = expire_date
        self.tokens_time_lock.release()

        self.tokens_ids_lock.release()
        return new_token

    # returns the user's id if token exists, -1 if not
    def remove_token(self, token: str) -> int:
        if self.is_token_exists(token):
            self.tokens_ids_lock.acquire()
            removed_id = self.tokens_ids[token]
            self.tokens_ids.pop(token)

            self.tokens_time_lock.acquire()
            self.tokens_expire_time.pop(token)
            self.tokens_time_lock.release()

            self.tokens_ids_lock.release()
            return removed_id
        return -1

    def is_token_expired(self, token: str) -> bool:
        self.tokens_time_lock.acquire()
        ret_val = self.tokens_expire_time[token] <= datetime.datetime.now()
        self.tokens_time_lock.release()
        return ret_val
