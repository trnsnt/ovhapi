import logging

LOGGER = logging.getLogger("ovhapi")


def setup_logger(logger):
    """
    Setup logger
    :param logger: Logger to setup
    :return: None
    """
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    logger.addHandler(logging.StreamHandler())
