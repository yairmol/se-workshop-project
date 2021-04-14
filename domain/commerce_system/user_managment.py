import threading

from domain.commerce_system.user import User


class UserManagement:
    management_lock = threading.Lock()

    def __init__(self, authenticator):
        self.active_users = {}
        self.authenticator = authenticator

    def add_active_user(self) -> int:
        new_user = User()
        token = self.authenticator.add_new_user_token(new_user.id)
        self.management_lock.acquire()
        self.active_users[new_user.id] = new_user
        self.management_lock.release()
        return token

    def remove_active_user(self, token):
        self.management_lock.acquire()
        user_id: int = self.authenticator.remove_token(token)
        if user_id > 0:
            if user_id in self.active_users:
                self.active_users.pop(user_id)
            else:
                print("LOG: Error - User's Token exists, but user object is missing ")
        else:
            print("LOG: Error - User's Token doesn't exists")
        self.management_lock.release()



