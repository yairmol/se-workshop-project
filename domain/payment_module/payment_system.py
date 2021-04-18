from domain.logger.log import event_logger


def pay(user_id: int, credit_card_number: int, expiration_date: int, card_holder_name: str) -> int:
    event_logger.info("LOG: Subscribed user: " + str(user_id) + " performed payment.")
    return True
