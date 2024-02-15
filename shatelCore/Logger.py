import logging
import sys


def GetStdoutLogger(logger_name: str):
    """
        return a stdout logger
    """
    formatter = logging.Formatter(
        "[APP-LOGGER <%(levelname)s> %(asctime)s]\n %(message)s\n %(module)s\nat line -%(lineno)d- in %(pathname)s "
    )
    logLevel = logging.INFO
    logger = logging.getLogger(logger_name)
    logger.setLevel(logLevel)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logLevel)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return handler
