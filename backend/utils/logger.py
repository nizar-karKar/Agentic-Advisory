import logging
import sys


def setup_logger(name: str = "agentic_app") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def log_node_execution(logger, node_name: str, iteration: int):
    logger.info(f"[NODE] {node_name} | iteration={iteration}")


def log_loop_end(logger, iteration: int, approved: bool):
    logger.info(
        f"[LOOP END] iteration={iteration} | approved={approved}"
    )
