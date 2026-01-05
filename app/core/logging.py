import logging
import sys

def setup_logging():
    # Create a root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    # Formatter (you can customize)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Add handler to root logger
    logger.addHandler(handler)
    return logger

logger = setup_logging()
