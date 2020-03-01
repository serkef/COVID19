""" custom utilities """

import logging
import os
from logging.handlers import TimedRotatingFileHandler
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import tweepy

from .config import (
    APP_LOGS,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_KEY_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    ENV,
)


def tweet_status(status):
    logging.info(f"Posting status {status!r}")

    if ENV == "production":
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_KEY_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        api.update_status(status)
    else:
        logging.info("Skipping - not in production")


def get_gsheet_api():
    """ Initializes Google API. Taken from quickstart example """

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "/home/serkef/Downloads/credentials.json",
                ["https://www.googleapis.com/auth/spreadsheets"],
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    return service.spreadsheets()


def set_logging(loglevel: [int, str] = "INFO"):
    """ Sets logging handlers """

    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(loglevel)

    APP_LOGS.mkdir(parents=True, exist_ok=True)
    log_path = f"{APP_LOGS / 'twitter-monitor.log'}"
    file_handler = TimedRotatingFileHandler(
        filename=log_path, when="midnight", encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(loglevel)

    errlog_path = f"{APP_LOGS / 'twitter-monitor.err'}"
    err_file_handler = TimedRotatingFileHandler(
        filename=errlog_path, when="midnight", encoding="utf-8"
    )
    err_file_handler.setFormatter(formatter)
    err_file_handler.setLevel(logging.WARNING)

    logger = logging.getLogger()
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.addHandler(err_file_handler)
    logger.setLevel(loglevel)
