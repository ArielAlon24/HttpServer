import logging


class LoggingHandler:
    LEVEL = logging.DEBUG
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @classmethod
    def create_logger(cls, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(cls.LEVEL)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(cls.LOG_FORMAT)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger
