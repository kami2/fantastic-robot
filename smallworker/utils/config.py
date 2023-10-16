import os
from dotenv import load_dotenv
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG = fr"{ROOT_DIR}\.env"
CONFIG = load_dotenv(DEFAULT_CONFIG)


def get_config(key: str):
    logging.info(f"Get environment variable {key}")
    return os.environ.get(key)

