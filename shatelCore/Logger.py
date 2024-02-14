import sys
import logging

def GetStdoutLogger():
    """
        return a stdout logger
    """
    formatter = logging.Formatter(
        "[APP-LOGGER <%(levelname)s> %(asctime)s]\n %(message)s\n %(module)s\nat line -%(lineno)d- in %(pathname)s "
    )
    logLevel = logging.INFO
    logger = logging.getLogger(__name__)
    logger.setLevel(logLevel)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logLevel)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return handler

