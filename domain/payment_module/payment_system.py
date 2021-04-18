from domain.logger.log import event_logger


def pay(user_id: int, **payment_details) -> int:
    event_logger.info("LOG: Subscribed user: " + str(user_id) + " performed payment.")
    return True
