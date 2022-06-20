# Making requests to govinfo api and web scraping

> This recipe shows how to make requests to the govinfo API, then use those response requests to get web pages we can then scrape to create a dataset of congressional texts.

**Problem Objective**: Build a dataset of all the congressional records between 2018 and 2020 to support our policy research project. 

Libraries required:

- `requests`
- `json`
- `BeautifulSoup`
- `pandas`

# Part 1 - Setup

The govinfo api is a free service provided by the U.S. Government Publishing Office for querying a large database of federal records. To use the api first get a token: [https://api.data.gov/signup/](https://api.data.gov/signup/). 

Try using some of api examples on https://api.govinfo.gov/docs/ - note that you must first hit "authorize" and provide your API key for them to work. 

Here's an example request, which asks the api for metadata about ```CREC-2018-01-04```:
```
https://api.govinfo.gov/packages/CREC-2018-01-04/summary?api_key=YOUR_API_KEY<---put your key in here!
```

In natural language, this translates to: 
> govinfo could you give me a summary of congressional record CREC-2018-01-04? 

Try copying this url into your web browser, and the api should display the following response on the web page for you:
```JSON
{
  "title": "Congressional Record Volume 164, Issue 2, (January 4, 2018)",
  "collectionCode": "CREC",
  "collectionName": "Congressional Record",
  "category": "Proceedings of Congress and General Congressional Publications",
  "dateIssued": "2018-01-04",
  "detailsLink": "https://www.govinfo.gov/app/details/CREC-2018-01-04",
  "granulesLink": "https://api.govinfo.gov/packages/CREC-2018-01-04/granules?offset=0&pageSize=100",
  "packageId": "CREC-2018-01-04",
  "download": {
    "pdfLink": "https://api.govinfo.gov/packages/CREC-2018-01-04/pdf",
    "pdfSenateLink": "https://api.govinfo.gov/packages/CREC-2018-01-04/pdf/senate",
    "pdfDailyDigestLink": "https://api.govinfo.gov/packages/CREC-2018-01-04/pdf/dailydigest",
    "modsLink": "https://api.govinfo.gov/packages/CREC-2018-01-04/mods",
    "premisLink": "https://api.govinfo.gov/packages/CREC-2018-01-04/premis",
    "zipLink": "https://api.govinfo.gov/packages/CREC-2018-01-04/zip"
  },
  "branch": "legislative",
  "pages": "48",
  "governmentAuthor1": "Congress",
  "suDocClassNumber": "X 1.1/A:, X/A.",
  "documentType": "CREC",
  "congress": "115",
  "session": "2",
  "volume": "164",
  "issue": "2",
  "bookCount": "1",
  "publisher": "U.S. Government Publishing Office",
  "otherIdentifier": {
    "migrated-doc-id": "cr04ja18",
    "ils-system-id": "000568013",
    "stock-number": "752-002-00000-2"
  },
  "lastModified": "2021-02-22T19:01:49Z"
}
```

There's a lot of information here, and part of becoming proficient in using an API is learning some of the API's unique terminology. Make a note of all the information we're provided here, and how the response we get here is similar to/different from other examples in the API documentation. 

Note that to use any of the download links you will need to affix your api key to the url:You can fix this by manually adding it to the url:
```
https://api.govinfo.gov/packages/CREC-2018-01-04/pdf?api_key=YOUR_API_KEY
```

Now that we have a basic understanding of how API's work, we can start to write some code that will automate this process of querying the api for us. We'll use pythons built in `requests` library for this.

# Part 2 - API Constraints and Automating Requests 

Here's an outline of our code:

1. Request the Package ID's of all the congressional records between 2018-01-01 and 2020-01-01
2. For each Package ID request the package metadata
3. From the package metadata retrieve a link the records transcript, then scrape this text
4. Construct a table the accounts for all of our data
5. Store the transcripts as .txt files

