"""
Shared logger configuration for the deployment module
"""
import logging
import sys

def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Sets up and returns a configured logger
    """
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s (%(levelname)s) - %(message)s"
    )
    return logging.getLogger(name)

logger = setup_logger()