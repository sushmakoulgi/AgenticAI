import logging

logger=logging.getLogger("AI_Agent")


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s |"
        "%(message)s" )
    )