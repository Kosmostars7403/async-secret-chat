import logging
import os


def setup_logger(name):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)
    return logger


def check_token_existence():
    if os.path.exists('token.txt'):
        with open('token.txt', 'r') as file:
            return file.read()
    return None




