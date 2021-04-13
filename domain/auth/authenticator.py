import secrets
import string


class Authenticator:
    alphabet = string.ascii_letters + string.digits

    def __init__(self):
        self.tokens_ids = {}

    def is_token_exists(self, token):
        return token in self.tokens_ids

    def generate_token(self, user_id):
        new_token = ''.join(secrets.choice(self.alphabet) for i in range(8))
        while self.is_token_exists(new_token):
            new_token = ''.join(secrets.choice(self.alphabet) for i in range(8))
        self.tokens_ids[new_token] = user_id




