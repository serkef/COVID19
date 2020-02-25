import logging
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from tabula import read_pdf

ENTRY_URL = (
    "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports/"
)
PDF_PATH = Path(__file__).parent / "situation_reports" / "pdf"
DATA_PATH = Path(__file__).parent / "situation_reports" / "data"
PDF_PATH.mkdir(parents=True, exist_ok=True)
DATA_PATH.mkdir(parents=True, exist_ok=True)


def download_report(pdf_url):
    """ Downloads a Situation Report PDF locally """

    filename = Path(pdf_url).name
    pdf_filepath = PDF_PATH / filename

    logging.info(f"Downloading {filename}")
    with open(pdf_filepath, "wb") as fout:
        res = requests.request("GET", pdf_url)
        fout.write(res.content)
    return pdf_filepath


def parse_report(pdf_filepath: Path):
    """ Extracts data from a local PDF and stores as csv """

    logging.info(f"Extracting data from {pdf_filepath.name}")

    data = read_pdf(pdf_filepath, pages="all")
    if type(data) is not list:
        data = [data]
    for idx, df in enumerate(data):
        df.to_csv(DATA_PATH / f"{pdf_filepath.stem}_{idx:02d}.csv")


def main():
    logging.basicConfig(level="INFO")

    situation_page = requests.get(ENTRY_URL)
    soup = BeautifulSoup(situation_page.text, "html.parser")
    for href in soup.find_all("a", href=re.compile(r".*\.pdf.*")):
        full_url = href["href"]
        url = urljoin(ENTRY_URL, urlparse(full_url).path)
        pdf_file = download_report(pdf_url=url)
        parse_report(pdf_file)


if __name__ == "__main__":
    main()
