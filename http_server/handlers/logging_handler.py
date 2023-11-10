"""
Name: Ariel Alon
Description: This module creates a 'LoggingHandler' for handling all the
             loggers that exist in this project.
"""

import logging


class LoggingHandler:
    """
    A class responsible for creating consistent loggers for each module.

    Attributes:
        LEVEL (int): The base level for all loggers.
        LOG_FORMAT (str): The format for all loggers.
    """

    LEVEL: int = logging.DEBUG
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @classmethod
    def create_logger(cls, name: str) -> logging.Logger:
        """
        Create a logger for a module.

        Parameters:
            name (str): The name of the module.

        Returns:
            logger (logging.Logger): The specific logger created.
        """
        logger = logging.getLogger(name)
        logger.setLevel(cls.LEVEL)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(cls.LOG_FORMAT)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger
