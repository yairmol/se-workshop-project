# Validation file
# need to update the validation conditions in the future

def validate_username(username: str) -> bool:
    return 0 < len(username) < 20


def validate_password(password: str) -> bool:
    return 0 < len(password) < 20
