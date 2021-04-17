# import logging
# logging.basicConfig(level = logging.INFO, filename = 'datacamp.txt')
# logging.debug("A Debug Logging Message")
# logging.info("A Info Logging Message")
# logging.warning("A Warning Logging Message")
# logging.error("An Error Logging Message")
# logging.critical("A Critical Logging Message")

import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# first file logger
event_logger = setup_logger('event_logger', 'event_log_file.log')
# event_logger.info('This is just info message')

# second file logger
error_logger = setup_logger('error_logger', 'error_log_file.log')
# error_logger.error('This is an error message')


# def another_method():
#     # using logger defined above also works here
#     logger.info('Inside method')
