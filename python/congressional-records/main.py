# Demonstrates using the govinfo API to download all the pdf transcripts of committee hearings between a given date
# range. Requires that you have an API key, to get one visit https://api.data.gov/signup/. Also see API documentation
# at https://api.govinfo.gov/docs/.

# web scraping
from bs4 import BeautifulSoup

# for making API requests
from urllib.request import Request, urlopen
import requests
import pandas as pd
import json

# for working with files and paths
import sys
import os

# for organizing and collecting our data
from pandas import DataFrame

# typing utilities
from typing import Any
from typing import List

# error handling
import traceback

# Your govinfo API key
OPEN_GOV_API_KEY = "mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5"

# Start of the time range for witch you would like documents
START_DATE = "2018-01-01"

# End of the time range for witch you would like documents
END_DATE = "2020-01-10"
# END_DATE = "2018-01-10" # Use this end date for debugging (returns <20 results)

# Category of documents you would like to collect. See bottom for list of different document types.
DOC_CATEGORY = "CHRG"

# Directory where will will save the transcripts
OUTPUT_DIR = "textfiles"

# Error log in case an API request fails
ERROR_LOG = "log.log"

# The GOV INFO  can only retrieve 100 records at a time. There are several thousand records in the CHRG category
# between 2018 and 2020. So we need to split up our records requests into several batches. So first we need to
# retrieve the total number of hearings for our time period.
def get_package_count(key: str, collection: str, start: str, end: str) -> int:
    url = 'https://api.govinfo.gov/published/{}/{}?offset=0&pageSize=100&collection={}&api_key={}'.format(start, end,
                                                                                                          collection,
                                                                                                          key)
    json_response = get_json(url)
    package_count = json_response["count"]
    print("retrieved {} record count for date range {}-{}: {}".format(collection, start, end, package_count))
    return int(json_response["count"])


# Every document, or "package", as they are referred to in the API, has a unique ID. We need to first get a documents
# ID in order to look up more information about it. For example, "LEGISLATIVE HEARING ON H.R. 4532, TO CREATE THE
# FIRST TRIBALLY MANAGED NATIONAL MONUMENT, AND FOR OTHER PURPOSES, ``SHASH JAA NATIONAL MONUMENT AND INDIAN CREEK
# NATIONAL MONUMENT ACT''--PART 1", has package id CHRG-115hhrg28219.
def getDocumentIds(key: str, collection: str, start: str, end: str, offset: int, count: int) -> List[DataFrame]:
    url = 'https://api.govinfo.gov/published/{}/{}?offset={}&pageSize={}&collection={}&api_key={}'.format(start, end,
                                                                                                          str(offset),
                                                                                                          str(count),
                                                                                                          collection,
                                                                                                          key)
    json_response = get_json(url)
    packages = json_response["packages"]
    packages_array = []
    # create a list of dataframes from the array of json objects
    for p in packages:
        df = pd.json_normalize(p)
        packages_array.append(df)
    print("retrieved ID Data for packages {}-{}".format(offset, offset + count))
    return packages_array


# Generates an initial dataframe for all of ours records, collecting information about 100 records at a time (again,
# because of the API limitations). The columns for the frame look like:
# [packageId|lastModified|packageLink|docClass|title|congress|dateIssued]
def generate_base_records_frame(key: str, collection: str, start: str, end: str, total_record_count: int):
    # floor divide by 100 to get the number of needed requests
    request_count = total_record_count // 100;
    id_array = []
    for x in range(0, request_count):
        ids = getDocumentIds(key, collection, start, end, x * 100, 100)
        id_array.append(ids)
    # get the remainder records
    id_array.append(
        getDocumentIds(key, collection, start, end, request_count * 100, total_record_count - request_count * 100))
    # merge all the dataframe arrays into a single 1d array
    flat_list = [item for sublist in id_array for item in sublist]
    base_record_frame = pd.concat(flat_list, ignore_index=True)
    print(base_record_frame)
    print("generated base record frame for dates {}-{}".format(start, end))
    return base_record_frame


# Using the id values from our base frame, we can now query specific information about the records we're interested
# in. In this function, for each row we request a "summary" of the package. Unfortunately the gov info api doesn't
# provide a direct means of getting the raw text of the record from an api response. However the summary does provide
# a link to a "mods" file, which is an XML summary of the document. This mods file contains a link to the raw html
# transcript of the document (See CHRG-115shrg36191/mods/xml for a mods file example). This link follows the formula:
# https://www.govinfo.gov/content/pkg/PACKAGE_ID/html/PACKAGE_ID.htm. We can then use beautifulsoup to scrape this
# page and get transcript text. See https://www.govinfo.gov/content/pkg/CHRG-115hhrg28219/html/CHRG-115hhrg28219.htm
# for an example.

def get_package_data(key: str, ids_frame):
    print("Now retrieving text for packages...")
    row_count = len(ids_frame)

    for index, row in ids_frame.iterrows():
        package_id = row["packageId"]

        # we'll save the package transcript as well as the package granules in .txt files
        transcript_file_path = "{}/{}.txt".format(OUTPUT_DIR, package_id)
        granules_file_path = "{}/{}_GRANULES.txt".format(OUTPUT_DIR, package_id)

        # put a link to the package summary in dataframe
        summary_url = 'https://api.govinfo.gov/packages/{}/summary?api_key={}'.format(package_id, key)
        ids_frame.loc[index, "summary_url"] = summary_url

        # write the scraped text to a .txt file
        record_url = "https://www.govinfo.gov/content/pkg/{}/html/{}.htm".format(package_id, package_id)
        record_html_text = scrape_page_text(record_url)
        write_txt(transcript_file_path, record_html_text)

        # get the mods link and zip link. The zip file will contain Useful for verification of the data.
        summary_json = get_json(summary_url)
        mods_link = summary_json["download"]["modsLink"]
        ids_frame.loc[index, "modsLink"] = mods_link
        pdf_link = summary_json["download"]["zipLink"]
        ids_frame.loc[index, "zipLink"] = pdf_link
        # https://api.govinfo.gov/packages/CHRG-107shrg82483/granules/CHRG-107shrg82483/summary?api_key=mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5
        # write the package granules to a .txt file
        granules_url = "https://api.govinfo.gov/packages/{}/granules/{}/summary?api_key={}".format(package_id,
                                                                                                   package_id, key)
        granules_json = get_json(granules_url)
        with open(granules_file_path, 'w') as f:
            json.dump(granules_json, f)

        # put the text file name into the dataframe
        ids_frame.loc[index, "text_file"] = transcript_file_path

        print("Retrieved html text data for record {}, {} of {} records".format(package_id, index,
                                                                                row_count))
    return ids_frame


# utilities
def frame_to_csv(frame, path: str) -> None:
    frame.to_csv(path, encoding="utf-8")


def get_json(url: str) -> Any:
    try:
        return requests.get(url).json()
    except Exception:
        with open("log.txt", "a") as log:
            traceback.print_exc(file=log)
        


def write_txt(path: str, text: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)



# Here we use the beautiful soup library to scrape text from an html page. For more about using beautiful soup see
# https://www.linkedin.com/learning/data-ingestion-with-python/working-with-beautiful-soup.
def scrape_page_text(url: str):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def clear_folder(path: str):
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))



def main():
    # clear our output directory
    clear_folder(OUTPUT_DIR)
    # get the number of packages (records) for our date range
    record_count = get_package_count(OPEN_GOV_API_KEY, DOC_CATEGORY, START_DATE, END_DATE)
    # get the ids for all of these packages
    package_id_frames = generate_base_records_frame(OPEN_GOV_API_KEY, DOC_CATEGORY, START_DATE, END_DATE, record_count)
    # using the package ids query the api for data about the package and retrieve the transcript
    package_data_frames = get_package_data(OPEN_GOV_API_KEY, package_id_frames)
    # export this data to a csv
    frame_to_csv(package_data_frames, "{}_RECORDS_{}-{}.csv".format(DOC_CATEGORY, START_DATE, END_DATE))

# main()

def test_request():
    url = "https://api.govinfo.gov/packages/CREC-2018-01-04/summary?api_key={}".format(OPEN_GOV_API_KEY)
    response = requests.get(url)
    print(response)
    # <Response [200]> // 200 = Valid response
    print(response.json())
    # {'title': 'Congressional Record Volume 164, Issue 2, (January 4, 2018)'...
    with open('test_response.json', 'w') as f:
        json.dump(response.json(), f)
    # see test_response.json

test_request()
# https://api.govinfo.gov/packages/CHRG-107shrg82483/granules/CHRG-107shrg82483/summary?api_key=mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5
# https://api.govinfo.gov/packages/CHRG-116shrg99104882/granules/CHRG-116shrg99104882/summary?api_key=mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5
# API EXAMPLES
# https://api.govinfo.gov/packages/CDOC-96sdoc27/summary?api_key={mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5}
# https://api.govinfo.gov/packages/CDOC-96sdoc27/mods?api_key=mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5
# https://api.govinfo.gov/packages/GPO-CONAN-2020-SUPP/summary?api_key=mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5
# https://api.govinfo.gov/packages/CREC-2018-01-04/zip?api_key=mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5
# https://api.govinfo.gov/packages/CREC-2018-01-04/pdf?api_key=mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5
# https://api.govinfo.gov/packages/CHRG-107shrg82483/granules/CHRG-107shrg82483/summary?api_key=mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5
# https://api.govinfo.gov/packages/CHRG-107shrg82483/granules?offset=0&pageSize=10&api_key=mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5
# https://api.govinfo.gov/packages/CREC-2018-01-04/granules?offset=0&pageSize=100?api_key=mHFrk52tb3tnJpM4Vn5M1Ydi4Sckac1ZrV5StAG5
