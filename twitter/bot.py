""" Monitoring entrypoint """

import logging
from time import sleep

from twitter.utilities import set_logging, tweet_status, get_gsheet_api
from twitter.config import (
    GSHEET_POLLING_INTERVAL_SEC,
    GSHEET_SPREADSHEET_ID,
    GSHEET_SHEET_NAME,
)

GSHEET_API = get_gsheet_api()


def fetch_daily_values():
    result = (
        GSHEET_API.values()
        .get(spreadsheetId=GSHEET_SPREADSHEET_ID, range=GSHEET_SHEET_NAME)
        .execute()
    )
    values = result.get("values", [])
    for col in range(1, min(len(values[0]), len(values[1]), len(values[2]))):
        date = values[0][col]
        value = values[1][col]
        monitor = values[2][col]

        if int(monitor):
            # Set monitor to False and yield
            values[2][col] = "0"
            GSHEET_API.values().update(
                spreadsheetId=GSHEET_SPREADSHEET_ID,
                range="DailyData!A3:AA3",
                valueInputOption="USER_ENTERED",
                body={"majorDimension": "ROWS", "values": [values[2]]},
            ).execute()
            yield date, value


def main():
    """ Main run function """

    logging.getLogger("googleapiclient.discovery").setLevel("WARNING")
    set_logging()
    logger = logging.getLogger(f"{__name__}.main")

    logger.info(f"Starting...")

    while True:
        for day, value in fetch_daily_values():
            tweet_status(f"Day: {day}, Value: {value}")

        logger.debug(f"Waiting {GSHEET_POLLING_INTERVAL_SEC} sec before polling gsheet")
        sleep(GSHEET_POLLING_INTERVAL_SEC)


if __name__ == "__main__":
    main()
