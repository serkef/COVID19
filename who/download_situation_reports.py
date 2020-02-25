import logging
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ENTRY_URL = (
    "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports/"
)
DOWNLOAD_PATH = Path(__file__).parent / "situation_reports" / "pdf"


def main():
    logging.basicConfig(level='INFO')

    situation_page = requests.get(ENTRY_URL)
    soup = BeautifulSoup(situation_page.text, "html.parser")
    for href in soup.find_all("a", href=re.compile(r".*\.pdf.*")):
        report_title = href.text
        logging.info(f"Downloading {report_title}")
        full_url = href["href"]
        url = urljoin(ENTRY_URL, urlparse(full_url).path)
        filename = Path(url).name
        pdf_filepath = DOWNLOAD_PATH / filename
        with open(pdf_filepath, "wb") as fout:
            res = requests.request("GET", url)
            fout.write(res.content)


if __name__ == "__main__":
    main()
