import os
from dotenv import load_dotenv
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG = fr"{ROOT_DIR}\.env"
CONFIG = load_dotenv(DEFAULT_CONFIG)


def get_config(key: str):
    env = os.environ.get(key)
    logging.info(f"Get environment variable {key} : {env}")
    return env

