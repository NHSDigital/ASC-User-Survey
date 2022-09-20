import logging


def setup_logging(loglevel="info") -> None:
    logging.basicConfig(
        level=loglevel.upper(),
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
    )
