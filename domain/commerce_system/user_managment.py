import domain.auth.authenticator.py

class UserManagement:

    def __init__(self):
        self.active_users = []

    def add_active_user(self) -> bool:
        new_user = User()
        self.active_users.append(new_user)
        return Authenticator.generate_token(new_user.id)



