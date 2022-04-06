# script for scraping articles from medium.com by tag for a given date range 
# iterates over the months in the year, and each day in a month to get the articles published on a day with the specified tags

from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen, Request
import pandas as pd
import time
#------------------------INPUTS-----------------------------------------------#

#to generalize this scraper for later use - EDIT THIS to suit your purposes
#keep all list items strings, or else this doesn't work
tags = ["health", "motherhood"] #tags to scrape
years = ['2020'] #years to scrape during
months = ['06' ] #months to scrape during (every available day within the month will be scraped)

yearsString = ''.join([str(yr) for yr in years])
monthsString = ''.join([str(month) for month in months])

NO_LIMIT = 10000000000

#every time we run the script we generate a .txt file that contains all the text from the articles we scraped
#we create a unique id based on the date range we've selected
unique_id = yearsString +"_" + monthsString +"_"
# use these values to limit the number of blog posts to collect, make it arbitrarily high (1000) if no limit
maxNumberDays = NO_LIMIT 

maxNumberOfArticles = NO_LIMIT # for no limit for number of articles to collect for a day
# maxNumberOfArticles = 10 #only tt

textName = "mediumText" + unique_id+".txt" #name of the output file

#don't touch unless you need to
hdr = {'User-Agent': 'Mozilla/5.0'}
t_start = time.time()

#------------------------SCRAPER FUNCTIONS------------------------------------#

# def checkProgress(inputFile, )
# generate the sheet links table
# search over text output file to see if article has already been scraped
# if it has already been scraped, then don't rescrape the article

#INPUT - components needed to get the start link
#OUTPUT - the links of all the articles in the tag in the date range
def scrapeLinksToArticles(tag, years, months):
    startLink = "https://medium.com/tag/"+tag+"/archive/"
    articleLinks = []
    for y in years:
        print("retrieving article links for year {}, tag {}".format(y, tag))
        yearLink = startLink + y
        for m in months:
            print("retrieving article links for year {}, month {}, tag, {}".format(y, m, tag))
            monLink = yearLink + "/" + m
            #open the month link and scrape all valid days (days w/ link) into drive
            req = Request(monLink,headers=hdr)
            page = urlopen(req)
            monSoup = BeautifulSoup(page, features="html.parser")
            try: #if there are days
                allDays = list(monSoup.find("div", {"class": "col u-inlineBlock u-width265 u-verticalAlignTop u-lineHeight35 u-paddingRight0"}).find_all("div", {"class":"timebucket"}))
                dayCount = 0
                for a in allDays:
                    if dayCount < maxNumberDays:
                        dayCount += 1
                        print("retrieving article links for year {}, month {}, day {}, tag {}".format(y, m, dayCount, tag))
                        try: #try to see if that day has a link
                            dayLink = a.find("a")['href']
                            req = Request(dayLink,headers=hdr)
                            page = urlopen(req)
                            daySoup = BeautifulSoup(page, features="html.parser")
                            links = list(daySoup.find_all("div", {"class": "postArticle-readMore"}))
                            dayArticleCount = 0
                            numLinks = len(links)
                            for l in links:
                                if dayArticleCount < maxNumberOfArticles:
                                    dayArticleCount += 1
                                    print("retrieving article link {}/{}, for year {}, month {}, day {}, tag {}".format(dayArticleCount, numLinks,y,
                                                                                                                  m,
                                                                                                                  dayCount,
                                                                                                                  tag))
                                    articleLinks.append(l.find("a")['href'])
                        except: pass
            except: #take the month's articles
                links = list(monSoup.find_all("div", {"class": "postArticle-readMore"}))
                for l in links:
                    articleLinks.append(l.find("a")['href'])
                print("issueHere")
    print("Article Links: ", len(articleLinks))
    # return [link 1, link2]
    # return [[link, health],
    return articleLinks

#INPUT - link to a medium article
#OUTPUT - string with all the article text
# find a way to add user credentails to the link before doing the scraping
def scrapeArticle(link):
    bodyText = ""
    # link = link+USER_CREDENTIALS
    req = Request(link,headers=hdr)
    try:
        page = urlopen(req)
        soup = BeautifulSoup(page, features="html.parser")
        textBoxes = list(soup.find("article").find_all("p"))
        for t in textBoxes:
            bodyText = bodyText + t.get_text()
    except urllib.error.URLError as e:
        error =  e.read().decode("utf8", 'ignore')
        print("failed to retrieve article, error {}".format(error))
    return bodyText

#------------------------PROCESS----------------------------------------------#

articleLinks = []
for tag in tags:
    articleLinks.extend(scrapeLinksToArticles(tag, years, months))
articleLinks = set(articleLinks) #get rid of any duplicates
# print(articleLinks)

# a+ = we're always going to add to the file
# w+ = overwrite the file from scratch
outPutText = open(textName, "w+", encoding='utf8')
count = 0
df = pd.DataFrame(articleLinks)

df.to_csv("article_links"+unique_id+".csv")
numArticles = len(articleLinks)

for art in articleLinks:
    outPutText.write(str('\n'))
    outPutText.write(str('\n'))
    outPutText.write(art)
    outPutText.write(str('\n'))
    outPutText.write(str('\n'))
    outPutText.write(str(scrapeArticle(art)))
    count += 1
    print("writing article {}/{} to {}".format(count, numArticles, art))
outPutText.close()

t_end = time.time()
elapsed_time =  t_end-t_start

print("Scraped {} articles in {} seconds".format(numArticles, elapsed_time))
