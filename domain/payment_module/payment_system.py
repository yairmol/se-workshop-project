from domain.logger.log import event_logger


def pay(foatcredit_card_number: int, expiration_date: int, card_holder_name: str, user_name: str):
    event_logger.info("LOG: Subscribed user: " + user_name + " performed payment.")