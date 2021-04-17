from domain.logger.log import event_logger


def deliver():
    event_logger.info("delivery")
