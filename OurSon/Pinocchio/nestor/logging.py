import logging, sys

def setup_logging(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        stream=sys.stdout,
    )

def get_logger(name: str):
    return logging.getLogger(name)
