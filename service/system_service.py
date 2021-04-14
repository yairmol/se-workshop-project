from domain.auth.authenticator import Authenticator
from domain.commerce_system.user_managment import UserManagement


class SystemService:

    def __init__(self):
        self.user_management = UserManagement(Authenticator())

    def enter(self) -> int:  # returns the new user's token
        return self.user_management.add_active_user()

    def exit(self, token: str):
        self.user_management.remove_active_user(token)

