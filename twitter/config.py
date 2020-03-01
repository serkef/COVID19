""" Main configuration and settings """

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# Log settings
APP_LOGS = Path(os.environ["APP_LOGS"])
APP_LOGLEVEL = os.getenv("APP_LOGLEVEL", "INFO")

# Secrets
TWITTER_CONSUMER_KEY = os.environ["CONSUMER_KEY"]
TWITTER_CONSUMER_KEY_SECRET = os.environ["CONSUMER_KEY_SECRET"]
TWITTER_ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
TWITTER_ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

GSHEET_POLLING_INTERVAL_SEC = int(os.getenv("APP_LOGLEVEL", "5"))
GSHEET_SPREADSHEET_ID = os.environ["GSHEET_SPREADSHEET_ID"]
GSHEET_SHEET_NAME = os.environ["GSHEET_SHEET_NAME"]

ENV = os.getenv("ENV", "testing")
