import os
from pathlib import Path

BASE_PATH = Path(__file__).parent

RAW_IMAGES_PATH = BASE_PATH / "raw" / "images"
RAW_TXT_PATH = BASE_PATH / "raw" / "txt"
LAST_PROCESSED_MESSAGE_ID_PATH = BASE_PATH / "raw" / "last_processed_message_id.txt"

DATASET_PATH = BASE_PATH / "datasets"
DATASET_JSON_PATH = BASE_PATH / "datasets" / "dataset.json"


OPENAI_API_KEY = os.environ.get("OPENAI_API")

TELEGRAM_API_ID = os.environ.get("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH")
TELEGRAM_SESSION_STRING = os.environ.get("TELEGRAM_SESSION_STRING")

TELEGRAM_CHANNEL_NAME = "kpszsu"

try:
    from local_config import *
except ImportError:
    pass
