# COVID-19

## World Health Organization
We download the Situation Reports regarding Coronavirus disease.

* `situation_reports.py` - Downloads and parses all reports (in pdf) from [who web page](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports/)

In order to run:
* Make sure you have python > 3.6 installed `python3 --version`
* Create a virtual environment `python3 -m venv venv/`
* Install all dependencies `pip install -r requirements.txt`
* Run the script `python3 situation_reports.py`


* All PDFs are in `who/situation_reports/pdf`
* All extracted CSVs are in `who/situation_reports/data`
