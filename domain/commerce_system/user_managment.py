from domain.commerce_system.user import User


class UserManagement:

    def __init__(self, authenticator):
        self.active_users = []
        self.authenticator = authenticator

    def add_active_user(self) -> int:
        new_user = User()
        self.authenticator.generate_token(new_user.id)
        self.active_users.append(new_user)
        return new_user.id



