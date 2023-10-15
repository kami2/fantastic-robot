import os
from dotenv import load_dotenv
import logging

CONFIG = load_dotenv(".env")


def get_config(key: str):
    logging.info(f"Get environment variable {key}")
    return os.environ.get(key)
