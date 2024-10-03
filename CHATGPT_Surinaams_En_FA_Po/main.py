# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import re
import sys
import time
import math
# import urllib2
# import urlparse
import optparse
import hashlib
# from cgi import escape
from traceback import format_exc

import scrapy
# from Queue import Queue, Empty as QueueEmpty
from bs4 import BeautifulSoup
import gevent
import asyncio
from lxml import html
from urllib.parse import urlparse
import os
# data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
from PIL import Image  # pillow library
import requests
import urllib.request
from gevent import Greenlet
from gevent import monkey
from selenium import webdriver
from lxml import etree
monkey.patch_socket()
import time
import requests
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
import scrapy

from lxml import etree
from bs4 import BeautifulSoup
import requests
from lxml import etree
import requests

# Set the number of links to crawl
num_links_to_crawl = 100

# Set the user agent to use for the request
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'

# Set the headers for the request
headers = {'User-Agent': user_agent}


# class WebCrawler:
#     def __init__(self,urls=[],num_worker = 1):
#         self.url_queue = Queue()
#         self.num_worker = num_worker
#     def worker(self,pid):
#         driver = self.initializeAnImegaDisabledDriver()  #initilize the webdirver
# #TODO catch the exception
#         while not self.url_queue.empty():
#             url = self.url_queue.get()
#             self.driver.get(url)
#             elem = self.driver.find_elements_by_xpath("//script | //iframe | //img") # get such element from webpage
#     def run(self):
#         jobs = [gevent.spawn(self.worker,i) for i in xrange(self.num_worker)]

def web(page, WebUrl):
    if (page > 0):
        url = WebUrl
        code = requests.get(url)
        plain = code.text

        s = BeautifulSoup(plain, "html.parser")
        for link in s.findAll("a", {"class": "s-access-detail-page"}):
            tet = link.get("title")
            print(tet)
            tet_2 = link.get("href")
            print(tet_2)


web(1, "https://www.remyvastgoed.com/104371")

HOME_PAGE = "https://www.remyvastgoed.com/104371"


def get_source(page_url):
    """
    A function to download the page source of the given URL.
    """
    r = requests.get(page_url)
    source = html.fromstring(r.content)

    return source


source = get_source(HOME_PAGE)
# li_list = source.xpath("//li[contains(@class, 'fpGridBox grid')]")
# item_names = [
#     li.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']") for li in li_list
# ]

# Lat-Lon of New York
# URL = "https://weather.com/weather/today/l/40.75,-73.98"
# resp = requests.get(URL)
# print(resp.status_code)
# print(resp.text)

# ################
# #
# #
# ################
# import io
# import pandas as pd
# import requests
#
# URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10YIE&cosd=2017-04-14&coed=2022-04-14"
# resp = requests.get(URL)
# if resp.status_code == 200:
#     csvtext = resp.text
#     csvbuffer = io.StringIO(csvtext)
#     df = pd.read_csv(csvbuffer)
#     print(df)

# ################
# #
# #
# ################
#
# import requests
#
# URL = "https://api.github.com/users/jbrownlee"
# resp = requests.get(URL)
# if resp.status_code == 200:
#     data = resp.json()
#     print(data)

# ################
# #
# #
# ################
# import requests
#
# URL = "https://en.wikipedia.org/static/images/project-logos/enwiki.png"
# wikilogo = requests.get(URL)
# if wikilogo.status_code == 200:
#     with open("enwiki.png", "wb") as fp:
#         fp.write(wikilogo.content)

# ################
# #
# #
# ################


# from lxml import etree
#
# # Create DOM from HTML text
# dom = etree.HTML(resp.text)
# # Search for the temperature element and get the content
# elements = dom.xpath("//span[@data-testid='TemperatureValue' and contains(@class,'CurrentConditions')]")
# print(elements[0].text)
# ################
# #
# #
# ################
# ...
# from bs4 import BeautifulSoup
#
# soup = BeautifulSoup(resp.text, "lxml")
# elements = soup.select('span[data-testid="TemperatureValue"][class^="CurrentConditions"]')
# print(elements[0].text)

# ################
# #
# #
# ################
# import requests
# from lxml import etree
#
# # Reading temperature of New York
# URL = "https://weather.com/weather/today/l/40.75,-73.98"
# resp = requests.get(URL)
#
# if resp.status_code == 200:
#     # Using lxml
#     dom = etree.HTML(resp.text)
#     elements = dom.xpath("//span[@data-testid='TemperatureValue' and contains(@class,'CurrentConditions')]")
#     print(elements[0].text)
#
#     # Using BeautifulSoup
#     soup = BeautifulSoup(resp.text, "lxml")
#     elements = soup.select('span[data-testid="TemperatureValue"][class^="CurrentConditions"]')
#     print(elements[0].text)

# ################
# #
# #
# ################
# import requests
#
# # Read Yahoo home page
# URL = "https://www.yahoo.com/"
# resp = requests.get(URL)
# dom = etree.HTML(resp.text)
#
# # Print news headlines
# elements = dom.xpath("//h3/a[u[@class='StretchedBox']]")
# for elem in elements:
#     print(etree.tostring(elem, method="text", encoding="unicode"))

# ################
# #
# #
# ################



HOME_PAGE = "https://www.remyvastgoed.com/104371"
URL = "https://www.remyvastgoed.com/104371"
resp = requests.get(URL)
# Create DOM from HTML text
dom = etree.HTML(resp.text)
domain = urlparse("https://www.remyvastgoed.com/102536").netloc
print(domain)
domain = urlparse("https://www.remax.sr/nl/woningen/koopwoningen/hs877/la-recontre-5e-straat.html").netloc
print(domain)
domain = urlparse("https://osonangadjari.com/properties/lelydorperweg-3/").netloc
print(domain)
domain = urlparse("https://www.affidata.com/sh/huizen-te-koop/surinam/woning/287794").netloc
print(domain)

site_links =["https://www.affidata.com/sh/huizen-te-koop/surinam/woning/487739",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463488",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463487",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463484",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463483",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463027",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463026",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463025",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463024",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463023",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463022",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463020",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463019",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463018",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463017",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463015",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/462922",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/462921",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/462918",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/462916",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/413870",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/408858",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/397523",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/397520",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/397519",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/397393",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/397392",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/394988",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/394680",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/394679",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/389950",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/384677",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/383922",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/381950",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/369100",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/368048",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/365186",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/363937",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/354268",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/353142",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/352716",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/350401",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/349659",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/343435",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/321950",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/321668",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/321184",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/320844",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/319833",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/316023",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/314600",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/309031",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/300751",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/300680",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/299776",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/299614",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/298919",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/295178",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/292072",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/288776",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/287794",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/286977",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/285386",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/283001",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/282788",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/281739",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/279744",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/15717",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/15492",
"https://www.affidata.com/sh/huizen-te-koop/surinam/woning/13029",
"https://osonangadjari.com/properties/lelydorperweg-3/",
"https://osonangadjari.com/properties/lelydorperweg-3/",
"https://osonangadjari.com/properties/vivian-ornastraat-2/",
"https://osonangadjari.com/properties/doebe-project-2/",
"https://osonangadjari.com/properties/monzonietstraat/",
"https://osonangadjari.com/properties/boeskikowtoe/",
"https://osonangadjari.com/properties/rampersadweg/",
"https://osonangadjari.com/properties/6569/",
"https://osonangadjari.com/properties/paragdhaniramsingweg/",
"https://osonangadjari.com/properties/vredenburg-serie-b/",
"https://osonangadjari.com/properties/johan-abdoelrahimstraat/",
"https://osonangadjari.com/properties/sahadewweg/",
"https://osonangadjari.com/properties/leiding-8-2/",
"https://osonangadjari.com/properties/ramanandweg/",
"https://osonangadjari.com/properties/leiding-11-2/",
"https://osonangadjari.com/properties/ethaanstraat-2/",
"https://osonangadjari.com/properties/ethaanstraat/",
"https://osonangadjari.com/properties/leiding-8-3/",
"https://osonangadjari.com/properties/indira-gandhiweg/",
"https://osonangadjari.com/properties/mangriestraat/",
"https://osonangadjari.com/properties/wanestraat/",
"https://osonangadjari.com/properties/elizabeths-hof/",
"https://osonangadjari.com/properties/pontbuiten/",
"https://osonangadjari.com/properties/jamaludinstraat/",
"https://osonangadjari.com/properties/vredenburg-serie-b-2/",
"https://osonangadjari.com/properties/talsmastraat/",
"https://osonangadjari.com/properties/tamanredjo/",
"https://osonangadjari.com/properties/morgenstond-3/",
"https://osonangadjari.com/properties/ringweg-noord-2/",
"https://osonangadjari.com/properties/bhoendeiweg/",
"https://osonangadjari.com/properties/bhramstraat/",
"https://osonangadjari.com/properties/robbylaan-2/",
"https://osonangadjari.com/properties/tajerbladweg/",
"https://osonangadjari.com/properties/welgedacht-a-2/",
"https://osonangadjari.com/properties/coesewijnestraat/",
"https://osonangadjari.com/properties/nbm-project/",
"https://osonangadjari.com/properties/estrellastraat/",
"https://osonangadjari.com/properties/10382/",
"https://osonangadjari.com/properties/brokopondolaan/",
"https://osonangadjari.com/properties/tweelingenweg/",
"https://osonangadjari.com/properties/zorg-en-hoop-5/",
"https://osonangadjari.com/properties/nieuw-weergevondenweg/",
"https://osonangadjari.com/properties/franchepanestraat-3/",
"https://osonangadjari.com/properties/abachiweg/",
"https://osonangadjari.com/properties/djitinderweg/",
"https://osonangadjari.com/properties/4e-rijweg/",
"https://osonangadjari.com/properties/welgedacht-c-3/",
"https://osonangadjari.com/properties/4400/",
"https://osonangadjari.com/properties/mohameddienweg/",
"https://osonangadjari.com/properties/watrakanoestraat/",
"https://osonangadjari.com/properties/charlesburg-3/",
"https://osonangadjari.com/properties/ecoresort/",
"https://osonangadjari.com/properties/1934/",
"https://osonangadjari.com/properties/margarethalaan/",
"https://osonangadjari.com/properties/15944/",
"https://osonangadjari.com/properties/15804/",
"https://osonangadjari.com/properties/kartaramstraat/",
"https://osonangadjari.com/properties/houtzagerij-saramaccakanaal/",
"https://osonangadjari.com/properties/assuriaproject/",
"https://osonangadjari.com/properties/swarankumar-baldewsingweg/",
"https://osonangadjari.com/properties/nijbroek-molgoweg/",
"https://osonangadjari.com/properties/marijkestraat/",
"https://osonangadjari.com/properties/14385/",
"https://osonangadjari.com/properties/6710/",
"https://osonangadjari.com/properties/hk-toevluchtwegchitoestr/",
"https://osonangadjari.com/properties/verlengde-welgedacht-a/",
"https://osonangadjari.com/properties/boedhiastraat/",
"https://osonangadjari.com/properties/aquariusstraat-5/",
"https://osonangadjari.com/properties/makelaar-breeveldstraat/",
"https://osonangadjari.com/properties/walabastraat/",
"https://osonangadjari.com/properties/8701/",
"https://osonangadjari.com/properties/boeskikowtu-straat-2/",
"https://osonangadjari.com/properties/cocobiacoweg/",
"https://osonangadjari.com/properties/abdoelstraat/",
"https://osonangadjari.com/properties/jibodh-project-4/",
"https://osonangadjari.com/properties/columbiastraat/",
"https://osonangadjari.com/properties/okrodam-2/",
"https://osonangadjari.com/properties/vijfde-rijweg-2/",
"https://osonangadjari.com/properties/sabanapark/",
"https://osonangadjari.com/properties/jos-josi-don-fowroestraat/",
"https://osonangadjari.com/properties/babunnootweg/",
"https://osonangadjari.com/properties/marsaweg/",
"https://osonangadjari.com/properties/anand-nagarweg/",
"https://osonangadjari.com/properties/8083/",
"https://osonangadjari.com/properties/spinnebloemstraat/",
"https://osonangadjari.com/properties/sidodadistraat/",
"https://osonangadjari.com/properties/wonderbladstraat-2/",
"https://osonangadjari.com/properties/jibodh-project/",
"https://osonangadjari.com/properties/clementineweg/",
"https://osonangadjari.com/properties/4639/",
"https://osonangadjari.com/properties/kalikastraat/",
"https://osonangadjari.com/properties/10634/",
"https://osonangadjari.com/properties/10295/",
"https://osonangadjari.com/properties/10007/",
"https://osonangadjari.com/properties/9925/",
"https://osonangadjari.com/properties/9519/",
"https://osonangadjari.com/properties/9538/",
"https://osonangadjari.com/properties/9446/",
"https://osonangadjari.com/properties/8678/",
"https://osonangadjari.com/properties/8379/",
"https://osonangadjari.com/properties/8354/",
"https://osonangadjari.com/properties/8150/",
"https://osonangadjari.com/properties/8113/",
"https://osonangadjari.com/properties/7522/",
"https://osonangadjari.com/properties/4824/",
"https://osonangadjari.com/properties/5786/",
"https://osonangadjari.com/properties/5877/",
"https://osonangadjari.com/properties/337/",
"https://osonangadjari.com/properties/5525/",
"https://osonangadjari.com/properties/5435/",
"https://osonangadjari.com/properties/5123/",
"https://osonangadjari.com/properties/4745/",
"https://osonangadjari.com/properties/3788/",
"https://osonangadjari.com/properties/3200/",
"https://www.remyvastgoed.com/104371",
"https://www.remyvastgoed.com/87042",
"https://www.remyvastgoed.com/72637",
"https://www.remyvastgoed.com/28103",
"https://www.remyvastgoed.com/101706",
"https://www.remyvastgoed.com/104552",
"https://www.remyvastgoed.com/101883",
"https://www.remyvastgoed.com/101693",
"https://www.remyvastgoed.com/101509",
"https://www.remyvastgoed.com/92433",
"https://www.remyvastgoed.com/104206",
"https://www.remyvastgoed.com/81396",
"https://www.remyvastgoed.com/104251",
"https://www.remyvastgoed.com/104161",
"https://www.remyvastgoed.com/103825",
"https://www.remyvastgoed.com/99394",
"https://www.remyvastgoed.com/92321",
"https://www.remyvastgoed.com/78175",
"https://www.remyvastgoed.com/103794",
"https://www.remyvastgoed.com/103543",
"https://www.remyvastgoed.com/103642",
"https://www.remyvastgoed.com/50568",
"https://www.remyvastgoed.com/91901",
"https://www.remyvastgoed.com/93599",
"https://www.remyvastgoed.com/99948",
"https://www.remyvastgoed.com/94033",
"https://www.remyvastgoed.com/36356",
"https://www.remyvastgoed.com/87535",
"https://www.remyvastgoed.com/102645",
"https://www.remyvastgoed.com/102536",
"https://www.remyvastgoed.com/102501",
"https://www.remyvastgoed.com/100859",
"https://www.remyvastgoed.com/100857",
"https://www.remyvastgoed.com/102301",
"https://www.remyvastgoed.com/102263",
"https://www.remyvastgoed.com/84295",
"https://www.remyvastgoed.com/59191",
"https://www.remyvastgoed.com/102027",
"https://www.remyvastgoed.com/63267",
"https://www.remyvastgoed.com/50737",
"https://www.remyvastgoed.com/100108",
"https://www.remyvastgoed.com/99869",
"https://www.remyvastgoed.com/101748",
"https://www.remyvastgoed.com/88937",
"https://www.remyvastgoed.com/97968",
"https://www.remyvastgoed.com/96799",
"https://www.remyvastgoed.com/95492",
"https://www.remyvastgoed.com/101104",
"https://www.remyvastgoed.com/100927",
"https://www.remyvastgoed.com/99323",
"https://www.remyvastgoed.com/100836",
"https://www.remyvastgoed.com/99293",
"https://www.remyvastgoed.com/99793",
"https://www.remyvastgoed.com/100709",
"https://www.remyvastgoed.com/100612",
"https://www.remyvastgoed.com/100633",
"https://www.remyvastgoed.com/69166",
"https://www.remyvastgoed.com/100560",
"https://www.remyvastgoed.com/54917",
"https://www.remyvastgoed.com/99703",
"https://www.remyvastgoed.com/82075",
"https://www.remyvastgoed.com/91839",
"https://www.remyvastgoed.com/86462",
"https://www.remyvastgoed.com/64803",
"https://www.remyvastgoed.com/96877",
"https://www.remyvastgoed.com/92905",
"https://www.remyvastgoed.com/99174",
"https://www.remyvastgoed.com/86077",
"https://www.remyvastgoed.com/98714",
"https://www.remyvastgoed.com/98593",
"https://www.remyvastgoed.com/98096",
"https://www.remyvastgoed.com/95566",
"https://www.remyvastgoed.com/96524",
"https://www.remyvastgoed.com/97692",
"https://www.remyvastgoed.com/97741",
"https://www.remyvastgoed.com/96879",
"https://www.remyvastgoed.com/97381",
"https://www.remyvastgoed.com/66899",
"https://www.remyvastgoed.com/83566",
"https://www.remyvastgoed.com/97243",
"https://www.remyvastgoed.com/97197",
"https://www.remyvastgoed.com/78861",
"https://www.remyvastgoed.com/97125",
"https://www.remyvastgoed.com/96811",
"https://www.remyvastgoed.com/70077",
"https://www.remyvastgoed.com/96587",
"https://www.remyvastgoed.com/96587",
"https://www.remyvastgoed.com/96679",
"https://www.remyvastgoed.com/96379",
"https://www.remyvastgoed.com/49563",
"https://www.remyvastgoed.com/96614",
"https://www.remyvastgoed.com/96136",
"https://www.remyvastgoed.com/96394",
"https://www.remyvastgoed.com/96299",
"https://www.remyvastgoed.com/95912",
"https://www.remyvastgoed.com/95693",
"https://www.remyvastgoed.com/93835",
"https://www.remyvastgoed.com/95319",
"https://www.remyvastgoed.com/94873",
"https://www.remyvastgoed.com/84441",
"https://www.remyvastgoed.com/44117",
"https://www.remyvastgoed.com/94197",
"https://www.remyvastgoed.com/87008",
"https://www.remyvastgoed.com/94157",
"https://www.remyvastgoed.com/94132",
"https://www.remyvastgoed.com/93731",
"https://www.remyvastgoed.com/93831",
"https://www.remyvastgoed.com/92852",
"https://www.remyvastgoed.com/87996",
"https://www.remyvastgoed.com/93555",
"https://www.remyvastgoed.com/93358",
"https://www.remyvastgoed.com/89041",
"https://www.remyvastgoed.com/93258",
"https://www.remyvastgoed.com/88824",
"https://www.remyvastgoed.com/48757",
"https://www.remyvastgoed.com/92979",
"https://www.remyvastgoed.com/82584",
"https://www.remyvastgoed.com/92625",
"https://www.remyvastgoed.com/39386",
"https://www.remyvastgoed.com/92712",
"https://www.remyvastgoed.com/91729",
"https://www.remyvastgoed.com/92545",
"https://www.remyvastgoed.com/91791",
"https://www.remyvastgoed.com/91915",
"https://www.remyvastgoed.com/91850",
"https://www.remyvastgoed.com/84017",
"https://www.remyvastgoed.com/52176",
"https://www.remyvastgoed.com/91446",
"https://www.remyvastgoed.com/59317",
"https://www.remyvastgoed.com/90550",
"https://www.remyvastgoed.com/91174",
"https://www.remyvastgoed.com/91113",
"https://www.remyvastgoed.com/84210",
"https://www.remyvastgoed.com/90973",
"https://www.remyvastgoed.com/90961",
"https://www.remyvastgoed.com/90954",
"https://www.remyvastgoed.com/90911",
"https://www.remyvastgoed.com/90876",
"https://www.remyvastgoed.com/90898",
"https://www.remyvastgoed.com/79829",
"https://www.remyvastgoed.com/90304",
"https://www.remyvastgoed.com/90120",
"https://www.remyvastgoed.com/90422",
"https://www.remyvastgoed.com/90237",
"https://www.remyvastgoed.com/90218",
"https://www.remyvastgoed.com/47411",
"https://www.remyvastgoed.com/90125",
"https://www.remyvastgoed.com/90149",
"https://www.remyvastgoed.com/89975",
"https://www.remyvastgoed.com/89872",
"https://www.remyvastgoed.com/89752",
"https://www.remyvastgoed.com/89365",
"https://www.remyvastgoed.com/89120",
"https://www.remyvastgoed.com/42332",
"https://www.remyvastgoed.com/89135",
"https://www.remyvastgoed.com/50168",
"https://www.remyvastgoed.com/58648",
"https://www.remyvastgoed.com/83560",
"https://www.remyvastgoed.com/88626",
"https://www.remyvastgoed.com/88511",
"https://www.remyvastgoed.com/84574",
"https://www.remyvastgoed.com/74262",
"https://www.remyvastgoed.com/78847",
"https://www.remyvastgoed.com/75654",
"https://www.remyvastgoed.com/88112",
"https://www.remyvastgoed.com/47192",
"https://www.remyvastgoed.com/87860",
"https://www.remyvastgoed.com/60824",
"https://www.remyvastgoed.com/87409",
"https://www.remyvastgoed.com/87193",
"https://www.remyvastgoed.com/87050",
"https://www.remyvastgoed.com/39461",
"https://www.remyvastgoed.com/34194",
"https://www.remyvastgoed.com/39743",
"https://www.remyvastgoed.com/86615",
"https://www.remyvastgoed.com/55923",
"https://www.remyvastgoed.com/55569",
"https://www.remyvastgoed.com/52166",
"https://www.remyvastgoed.com/52052",
"https://www.remyvastgoed.com/68693",
"https://www.remyvastgoed.com/68967",
"https://www.remyvastgoed.com/86027",
"https://www.remyvastgoed.com/85922",
"https://www.remyvastgoed.com/49055",
"https://www.remyvastgoed.com/72126",
"https://www.remyvastgoed.com/85249",
"https://www.remyvastgoed.com/84917",
"https://www.remyvastgoed.com/84764",
"https://www.remyvastgoed.com/84257",
"https://www.remyvastgoed.com/82745",
"https://www.remyvastgoed.com/83827",
"https://www.remyvastgoed.com/83842",
"https://www.remyvastgoed.com/83712",
"https://www.remyvastgoed.com/83732",
"https://www.remyvastgoed.com/83557",
"https://www.remyvastgoed.com/83393",
"https://www.remyvastgoed.com/83303",
"https://www.remyvastgoed.com/55543",
"https://www.remyvastgoed.com/77782",
"https://www.remyvastgoed.com/83010",
"https://www.remyvastgoed.com/82726",
"https://www.remyvastgoed.com/82644",
"https://www.remyvastgoed.com/81421",
"https://www.remyvastgoed.com/5390",
"https://www.remyvastgoed.com/81817",
"https://www.remyvastgoed.com/63639",
"https://www.remyvastgoed.com/75999",
"https://www.remyvastgoed.com/81451",
"https://www.remyvastgoed.com/81133",
"https://www.remyvastgoed.com/40537",
"https://www.remyvastgoed.com/79482",
"https://www.remyvastgoed.com/76539",
"https://www.remyvastgoed.com/78058",
"https://www.remyvastgoed.com/962",
"https://www.remyvastgoed.com/78424",
"https://www.remyvastgoed.com/78265",
"https://www.remyvastgoed.com/16393",
"https://www.remyvastgoed.com/77698",
"https://www.remyvastgoed.com/77348",
"https://www.remyvastgoed.com/76408",
"https://www.remyvastgoed.com/77117",
"https://www.remyvastgoed.com/36795",
"https://www.remyvastgoed.com/76545",
"https://www.remyvastgoed.com/37750",
"https://www.remyvastgoed.com/76133",
"https://www.remyvastgoed.com/51158",
"https://www.remyvastgoed.com/75469",
"https://www.remyvastgoed.com/75412",
"https://www.remyvastgoed.com/32753",
"https://www.remyvastgoed.com/74958",
"https://www.remyvastgoed.com/74818",
"https://www.remyvastgoed.com/74469",
"https://www.remyvastgoed.com/74511",
"https://www.remyvastgoed.com/74275",
"https://www.remyvastgoed.com/71928",
"https://www.remyvastgoed.com/74287",
"https://www.remyvastgoed.com/68364",
"https://www.remyvastgoed.com/74062",
"https://www.remyvastgoed.com/73259",
"https://www.remyvastgoed.com/73261",
"https://www.remyvastgoed.com/35424",
"https://www.remyvastgoed.com/72492",
"https://www.remyvastgoed.com/8279",
"https://www.remyvastgoed.com/71668",
"https://www.remyvastgoed.com/71727",
"https://www.remyvastgoed.com/28983",
"https://www.remyvastgoed.com/70004",
"https://www.remyvastgoed.com/69645",
"https://www.remyvastgoed.com/69096",
"https://www.remyvastgoed.com/68794",
"https://www.remyvastgoed.com/68816",
"https://www.remyvastgoed.com/68827",
"https://www.remyvastgoed.com/35563",
"https://www.remyvastgoed.com/45740",
"https://www.remyvastgoed.com/68016",
"https://www.remyvastgoed.com/67928",
"https://www.remyvastgoed.com/66988",
"https://www.remyvastgoed.com/64171",
"https://www.remyvastgoed.com/66767",
"https://www.remyvastgoed.com/66485",
"https://www.remyvastgoed.com/66166",
"https://www.remyvastgoed.com/66360",
"https://www.remyvastgoed.com/66010",
"https://www.remyvastgoed.com/62676",
"https://www.remyvastgoed.com/65544",
"https://www.remyvastgoed.com/65223",
"https://www.remyvastgoed.com/55921",
"https://www.remyvastgoed.com/65089",
"https://www.remyvastgoed.com/65028",
"https://www.remyvastgoed.com/63818",
"https://www.remyvastgoed.com/59825",
"https://www.remyvastgoed.com/62310",
"https://www.remyvastgoed.com/62094",
"https://www.remyvastgoed.com/62029",
"https://www.remyvastgoed.com/61588",
"https://www.remyvastgoed.com/61324",
"https://www.remyvastgoed.com/33801",
"https://www.remyvastgoed.com/60098",
"https://www.remyvastgoed.com/41831",
"https://www.remyvastgoed.com/59431",
"https://www.remyvastgoed.com/58292",
"https://www.remyvastgoed.com/57757",
"https://www.remyvastgoed.com/39775",
"https://www.remyvastgoed.com/50827",
"https://www.remyvastgoed.com/56667",
"https://www.remyvastgoed.com/44891",
"https://www.remyvastgoed.com/55840",
"https://www.remyvastgoed.com/55363",
"https://www.remyvastgoed.com/54825",
"https://www.remyvastgoed.com/54402",
"https://www.remyvastgoed.com/49626",
"https://www.remyvastgoed.com/52887",
"https://www.remyvastgoed.com/41453",
"https://www.remyvastgoed.com/50669",
"https://www.remyvastgoed.com/51321",
"https://www.remyvastgoed.com/49582",
"https://www.remyvastgoed.com/48755",
"https://www.remyvastgoed.com/48467",
"https://www.remyvastgoed.com/48296",
"https://www.remyvastgoed.com/48075",
"https://www.remyvastgoed.com/46261",
"https://www.remyvastgoed.com/46109",
"https://www.remyvastgoed.com/45411",
"https://www.remyvastgoed.com/45332",
"https://www.remyvastgoed.com/14805",
"https://www.remyvastgoed.com/43093",
"https://www.remyvastgoed.com/42864",
"https://www.remyvastgoed.com/42389",
"https://www.remyvastgoed.com/40517",
"https://www.remyvastgoed.com/7500",
"https://www.remyvastgoed.com/39234",
"https://www.remyvastgoed.com/38601",
"https://www.remyvastgoed.com/38506",
"https://www.remyvastgoed.com/38252",
"https://www.remyvastgoed.com/38320",
"https://www.remyvastgoed.com/38308",
"https://www.remyvastgoed.com/37544",
"https://www.remyvastgoed.com/35997",
"https://www.remyvastgoed.com/35489",
"https://www.remyvastgoed.com/34880",
"https://www.remyvastgoed.com/34827",
"https://www.remyvastgoed.com/34279",
"https://www.remyvastgoed.com/30194",
"https://www.remyvastgoed.com/29580",
"https://www.remyvastgoed.com/29257",
"https://www.remyvastgoed.com/28822",
"https://www.remyvastgoed.com/16247",
"https://www.remyvastgoed.com/15603",
"https://www.remyvastgoed.com/12867",
"https://www.remyvastgoed.com/12690",
"https://www.remyvastgoed.com/12271",
"https://www.remyvastgoed.com/4692",
"https://www.remyvastgoed.com/4692",
"https://www.remyvastgoed.com/27810",
"https://www.mahanvastgoed.com/property/okro-uduweg-te-wanica/",
"https://www.mahanvastgoed.com/property/zwartenhovenburgstraat-te-paramaribo/",
"https://www.mahanvastgoed.com/property/kwattaweg-te-paramaribo-3/",
"https://www.mahanvastgoed.com/property/kwattaweg-te-paramaribo/",
"https://www.mahanvastgoed.com/property/nejalweg-te-wanica/",
"https://www.mahanvastgoed.com/property/mamboelastraat-te-paramaribo/",
"http://www.apurahousing.com/uitgebreidzoeken.aspx?zoekenop=va&st1=1&st2=1&pi=2",
"https://www.remax.sr/nl/woningen/koopwoningen/hs893/poerwodadi-weg.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs894/hendrikstraat-47.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs890/rahemal-70a.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs734/sadiodam-34.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs889/indira-gandhiweg.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs888/izaak-burnetstraat-69.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs875/chinitiestraat.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs887/kapitein-a-philipstraat-49.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs886/pommerosestraat-6.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs854/idoeweg-no-44.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs859/karanweg.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs884/chopinstraat-83.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs779/grandostraat-53.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs883/advocaatstraat-11.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs820/verkocht/laan-van-vertrouwen-pc-84b-gated-community.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs881/stippelvarensweg.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs793/oost-westverbinding-tamansari.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs874/calliopsestraat-12.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs858/verkocht/koolestraat-72.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs879/gated-community-villa-park-kwatta-waterkersstraat-50.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs699/anniestraat-32-hoek-hardeveldstraat.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs750/khadiweg-45.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs877/la-recontre-5e-straat.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs878/gogomangostraat-17.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs815/rijsdijkweg-462.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs871/monizstraat-5-bennies-park.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs872/la-recontre-4e-straat.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs831/tweelingenweg-hoek-steenbokweg.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs861/wc-kennedystraat-9.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs397/hugostraat-13.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs870/bhattoeweg-178a.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs707/chamroeweg-89.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs862/laan-van-louiseshof-38.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs805/prodjosoekartoweg-21-lelydorp.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs866/razabsekhweg-42-46.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs855/masoesastraat-31.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs674/lakeland-tout-lui-faut-colettelaan-13.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs840/baboe-sewrajsingweg-43.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs826/saltatiestraat-26.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs819/goosenweg-34-vredenburg-serie-b.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs637/bhattoeweg-178.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs860/mosstraat-3.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs856/eikvarensweg-10-12.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs795/ro-carstersstraat-16.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs848/woonproject-catharina-sophia-no-11.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs828/panchamweg-8.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs736/eduardstraat-24.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs851/boekoestraat-hoek-kwamikondrestraat.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs702/zegellakpalmlaan-29-palm-village.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs846/gompertsstraat-166.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs845/soepgroenteweg-71.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs785/verkocht/laan-van-steendam-07-gated-community-de-schuilplaats.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs774/vredenburgweg-56.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs749/zwartebondstraat-116-reeberg-project.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs835/fabrikaatstraat-88.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs806/helstonestraat-11-hoek-sewbarath-misserstraat.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs780/welgedacht-a-weg-394b.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs782/porfierstraat-39.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs813/lashkarweg-78-a-omgeving-vierde-rijweg.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs741/commissaris-roblesweg-pc-413-commewijne.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs827/eusieweg-6.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs824/leiding-8-br-139.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs791/laan-van-nobelheid.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs766/saprapiweg-3.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs685/sitalweg-109.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs787/afobakalaan-7-hoek-phedralaan.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs810/kankawastraat-19-zijstraat-toekomstweg.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs755/overbrugweg-10.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs796/bananenweg-87-jarikaba.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs747/wicherstraat-35.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs527/colony-31.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs801/hardwarsingweg-04.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs799/mangolaan-86c.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs783/gonggrijpstraat-184.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs781/maanviweg-19-welgedacht-b.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs776/surya-nagarweg-12.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs705/bieslookstraat-2.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs772/hoek-uranus-en-plejadenstraat-62.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs771/eusieweg-38.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs770/boxel-sir-winston-churchillweg-673.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs733/hanna-slustweg-149.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs753/weg-naar-reeberg-112.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs744/cordialaan-21.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs313/etnalaan-19.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs618/nijbroek-molgoweg-21.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs725/braamshoopweg-04.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs743/segansistraat-08.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs727/anton-mauvestraat-02-hoek-mesdagstraat-07.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs730/patnaweg-29.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs724/van-brussellaan-14.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs728/van-varseveldweg-30.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs489/monzonietstraat-3.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs700/mangrovestraat-17.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs713/eusieweg-39.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs651/commissarisweg-9.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs719/tayerbladweg-06-district-saramacca.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs596/fijne-klaroenweg-25.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs687/stondoifistraat-9-hoek-sriostraat.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs693/curacao-de-nederlandse-antillen.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs622/anton-dragtenweg.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs588/perzikbonenweg-302.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs660/javaweg-perc-199.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs679/overbrugweg-24.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs528/ramalaan-37.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs577/hardwarsingweg-28.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs404/powisistraat-109.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs476/kwattaweg-28.html",
"https://www.remax.sr/nl/woningen/koopwoningen/hs491/commissaris-weytinghweg-59i.html"]
#

elements = dom.xpath("//*[@id=""top_section""]/h2[1]")
#(elements)

soup = BeautifulSoup(resp.text, "lxml")
elements = soup.select('#top_section > h2.title')
print(elements[0].string)

class TrafficLight:
    '''This is an updated traffic light class'''
    def __init__(self, color):
        self.color = color

    def action(self):
        if self.color=='red':
            print('Stop & wait')
        elif self.color=='yellow':
            print('Prepare to stop')
        elif self.color=='green':
            print('Go')
        else:
            print('Stop drinking 😉')


class Dog:

    kind = 'canine'         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)

    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)

    __update = update   # private copy of original update() method


from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    dept: str
    salary: int


class MappingSubclass(Mapping):

    def update(self, keys, values):
        # provides new signature for update()
        # but does not break __init__()
        for item in zip(keys, values):
            self.items_list.append(item)


class Bag:
    def __init__(self):
        self.data = []

    def add(self, x):
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)
        self.add(x)


class DerivedClassName(Bag, MappingSubclass, Employee):
    def __init__(self):
        self.data = []

    def add(self, x):
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)
        self.add(x)




class Crawler:
    name: str
    dept: str
    salary: int

    def __init__(self):
        self.data = []

    def add(self, x):
        self.data.append(x)

    def validateURL(self, url):
        return url


    def findWebsite(self,url):
        try:
            domain = urlparse(url).netloc
            print(domain)
            if not resp.status_code == 200: raise Exception()
        except (Exception):
            print("Website is not up")
        return url

    def findPagination(self,url):
        return url

    def makeListOfFoubndLinks(self,url):
        return url

    def findImage(self,url):
        return url

    def imageName(self,url):
        return url

    def downloadImage(self,url):
        return url

    def findStreetName(self,url):
        soup = BeautifulSoup(resp.text, "lxml")
        straatnaam = soup.select('#top_section > h2.title')
        print(straatnaam[0].string)
        return url

    def findHouseNumer(self,url):
        return url

    def findPostalCode(self,url):
        return url

    def findNumberOfRooms(self,url):
        return url

    def findPerceel(self,url):
        soup = BeautifulSoup(resp.text, "lxml")
        elements = soup.select(
            '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(3) > td:nth-child(2)')
        print(elements)
        return url

    def findBouwoppervlakte(self,url):
        soup = BeautifulSoup(resp.text, "lxml")
        elements = soup.select(
            '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(4) > td:nth-child(2)')
        print(elements)
        return url

    def findVraagprijs(self,url):
        source = get_source(HOME_PAGE)
        resp = requests.get(URL)
        dom = etree.HTML(resp.text)
        soup = BeautifulSoup(resp.text, "lxml")
        elements = soup.select('#top_section > h2.prijs')
        print(elements[0].text)
        return url

    def findImfindAantal_kamers(self,url):
        soup = BeautifulSoup(resp.text, "lxml")
        elements = soup.select(
            '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(5) > td:nth-child(2)')
        print(elements)
        return url

    def find_aantal_Slaapkamers(self,url):
        soup = BeautifulSoup(resp.text, "lxml")
        elements = soup.select(
            '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(6) > td:nth-child(2)')
        print(elements)
        return url

    def findImage(self,url):
        divs = soup.findAll("galleria-image")
        print(divs)
        divs = soup.findAll("galleria-images")
        print(divs)
        divs = soup.findAll("table", {"class": "kenmerken"})
        print(divs)
        images = soup.find_all('img')
        print(images)
        images_url = images[0]['src']
        images = soup.findAll('img')
        for image in images:
            print(image['src'])

        # images_url
        # print(images_url)
        # #data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
        # from PIL import Image #pillow library
        # import requests
        # import urllib.request

        # im = Image.open(requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg", stream=True).raw)

        # Opening a new file named img with extension .jpg
        # This file would store the data of the image file
        # f = open('img.jpg', 'wb')
        # # Storing the image data inside the data variable to the file
        # f.write(im)
        # f.close()
        # img_data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
        # with open('netflix.jpg', 'wb') as handler:
        #     handler.write(img_data)
        # with open('pic1.jpg', 'wb') as handle:
        #     response = requests.get('www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg', stream=True)
        #
        #     if not response.ok:
        #         print(response)
        #
        #     for block in response.iter_content(1024):
        #         if not block:
        #             break
        #
        #         handle.write(block)
        # urllib.request.urlretrieve(
        #     'remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg',
        #     "gfg.png")
        #
        # img = Image.open("gfg.png")
        # img.show()

        # find image with '1-' and  followed up with any number that ends with .jpg
        r = requests.get("http://www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg", allow_redirects=True)
        image_name = straatnaam[0].string + ".jpg"
        open(image_name, 'wb').write(r.content)
        print(straatnaam[0].string, type, title, Perceeloppervlakte, Bouwoppervlakte, aantal_kamers, aantal_slaapkamers)
        line = straatnaam[
                   0].string + "," + type + "," + title + "," + Perceeloppervlakte + "," + Bouwoppervlakte + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
        with open('somefile.txt', 'a') as the_file:
            the_file.write(line)

        divs = soup.findAll("table", {"class": "kenmerken"})
        for div in divs:
            row = ''
            rows = div.findAll('tr')
            for row in rows:
                print(row)
                # if (row.text.find("PHONE") > -1):
                #     print(row.text)

        # li_list = source.xpath("//li[contains(@class, 'fpGridBox grid')]")
        # item_names = [
        #     li.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']") for li in li_list
        # ]
        return url

    def makeRowLineOfFile(self,url):
        soup = BeautifulSoup(resp.text, "lxml")
        elements = soup.select('#bottom_section > div > div.kenmerken')
        print(elements[0])
        type = (soup.find("td", text="Type").find_next_sibling("td").string)
        print(type)
        title = (soup.find("td", text="Titel").find_next_sibling("td").string)
        print(title)
        Perceeloppervlakte = (soup.find("td", text="Perceeloppervlakte").find_next_sibling("td").string)
        print(Perceeloppervlakte)
        Bouwoppervlakte = (soup.find("td", text="Bouwoppervlakte").find_next_sibling("td").string)
        print(Bouwoppervlakte)
        aantal_kamers = (soup.find("td", text="Aantal kamers").find_next_sibling("td").string)
        print(aantal_kamers)
        aantal_slaapkamers = (soup.find("td", text="Aantal slaapkamers").find_next_sibling("td").string)
        print(aantal_slaapkamers)
        return url

    def makeRowLineOfFile(self, url):
        if resp.status_code == 200:
            # Using straatnaam
            dom = etree.HTML(resp.text)
            straatnaam = dom.xpath("//*[@id=""top_section""]/h2[1]")
            print(straatnaam)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            straatnaam = soup.select('#top_section > h2.title')
            print(straatnaam[0].string)

            # Using prijs
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""top_section""]/h2[2]")
            print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select('#top_section > h2.prijs')
            print(elements[0].text)

            # Using kamers
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""bottom_section""]/div/div[1]/table/tbody/tr[5]/td[2]")
            print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select(
                '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(5) > td:nth-child(2)')
            print(elements)

            # Using slaapkamers
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""bottom_section""]/div/div[1]/table/tbody/tr[6]/td[2]")
            print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select(
                '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(6) > td:nth-child(2)')
            print(elements)

            # Using perceeloppervlakte
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""bottom_section""]/div/div[1]/table/tbody/tr[3]/td[2]")
            print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select(
                '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(3) > td:nth-child(2)')
            print(elements)

            # Using bouwoppervlakte
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""bottom_section""]/div/div[1]/table/tbody/tr[4]/td[2]")
            print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select(
                '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(4) > td:nth-child(2)')
            print(elements)

            # Using class
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""bottom_section""]/div/div[1]")
            # print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select('#bottom_section > div > div.kenmerken')
            print(elements[0])
            type = (soup.find("td", text="Type").find_next_sibling("td").string)
            print(type)
            title = (soup.find("td", text="Titel").find_next_sibling("td").string)
            print(title)
            Perceeloppervlakte = (soup.find("td", text="Perceeloppervlakte").find_next_sibling("td").string)
            print(Perceeloppervlakte)
            Bouwoppervlakte = (soup.find("td", text="Bouwoppervlakte").find_next_sibling("td").string)
            print(Bouwoppervlakte)
            aantal_kamers = (soup.find("td", text="Aantal kamers").find_next_sibling("td").string)
            print(aantal_kamers)
            aantal_slaapkamers = (soup.find("td", text="Aantal slaapkamers").find_next_sibling("td").string)
            print(aantal_slaapkamers)

            # print("a={0}".format(straatnaam))
            # print(b"hi there, straatnaam=%s\n,  ", straatnaam)
            # print("hi there, straatnaam=%s\n", straatnaam)
            # print("Hello, this is my name %s and my age %d", "Martin", 20)

            divs = soup.findAll("galleria-image")
            print(divs)
            divs = soup.findAll("galleria-images")
            print(divs)
            divs = soup.findAll("table", {"class": "kenmerken"})
            print(divs)
            images = soup.find_all('img')
            print(images)
            images_url = images[0]['src']
            images = soup.findAll('img')
            for image in images:
                print(image['src'])

            # images_url
            # print(images_url)
            # #data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
            # from PIL import Image #pillow library
            # import requests
            # import urllib.request

            # im = Image.open(requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg", stream=True).raw)

            # Opening a new file named img with extension .jpg
            # This file would store the data of the image file
            # f = open('img.jpg', 'wb')
            # # Storing the image data inside the data variable to the file
            # f.write(im)
            # f.close()
            # img_data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
            # with open('netflix.jpg', 'wb') as handler:
            #     handler.write(img_data)
            # with open('pic1.jpg', 'wb') as handle:
            #     response = requests.get('www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg', stream=True)
            #
            #     if not response.ok:
            #         print(response)
            #
            #     for block in response.iter_content(1024):
            #         if not block:
            #             break
            #
            #         handle.write(block)
            # urllib.request.urlretrieve(
            #     'remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg',
            #     "gfg.png")
            #
            # img = Image.open("gfg.png")
            # img.show()

            # find image with '1-' and  followed up with any number that ends with .jpg
            r = requests.get("http://www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg", allow_redirects=True)
            image_name = straatnaam[0].string + ".jpg"
            open(image_name, 'wb').write(r.content)
            print(straatnaam[0].string, type, title, Perceeloppervlakte, Bouwoppervlakte, aantal_kamers,
                  aantal_slaapkamers)
            line = straatnaam[
                       0].string + "," + type + "," + title + "," + Perceeloppervlakte + "," + Bouwoppervlakte + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
            with open('somefile.txt', 'a') as the_file:
                the_file.write(line)

            divs = soup.findAll("table", {"class": "kenmerken"})
            for div in divs:
                row = ''
                rows = div.findAll('tr')
                for row in rows:
                    print(row)
                    # if (row.text.find("PHONE") > -1):
                    #     print(row.text)

            # li_list = source.xpath("//li[contains(@class, 'fpGridBox grid')]")
            # item_names = [
            #     li.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']") for li in li_list
            # ]
        return url






for web_url in site_links :
    if re.search('remyvastgoed.com', web_url):
        print(web_url)
        if resp.status_code == 200:
            # ################
            # #
            # #
            # ################
            URL = web_url
            resp = requests.get(URL)
            soup = BeautifulSoup(resp.text, "lxml")

            divs = soup.findAll("table", {"class": "kenmerken"})
            # for div in divs:
            #     row = ''
            #     rows = div.findAll('td')
            #     for row in rows:
            #         print(row[0].string)
            #         print(row[1].string)
            # ################
            # #
            # #
            # ################
            # Using straatnaam
            soup = BeautifulSoup(resp.text, "lxml")
            straatnaam = soup.select('#top_section > h2.title')
            print(straatnaam[0].string)

            # Using prijs
            prijs = soup.select('#top_section > h2.prijs')
            print(prijs[0].text)

            # # Using kamers
            # aantal_kamers = soup.select(
            #     '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(5) > td:nth-child(2)')
            # print(aantal_kamers)
            #
            # # Using slaapkamers
            # aantal_slaapkamers = soup.select(
            #     '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(6) > td:nth-child(2)')
            # print(aantal_slaapkamers)
            #
            # # Using perceeloppervlakte
            # perceel_opp = soup.select(
            #     '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(3) > td:nth-child(2)')
            # print(perceel_opp)
            #
            # # Using bouwoppervlakte
            # bouwoppervlakte = soup.select(
            #     '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(4) > td:nth-child(2)')
            # print(bouwoppervlakte)

            # ################
            # #
            # #
            # ################
            # soup = BeautifulSoup(resp.text, "lxml")
            # elements = soup.select('#bottom_section > div > div.kenmerken')
            # print(elements[0])
            type = (soup.find("td", text="Type").find_next_sibling("td").string)
            print(type)
            title = (soup.find("td", text="Titel").find_next_sibling("td").string)
            print(title)
            Perceeloppervlakte = (soup.find("td", text="Perceeloppervlakte").find_next_sibling("td").string)
            print(Perceeloppervlakte)
            Bouwoppervlakte = (soup.find("td", text="Bouwoppervlakte").find_next_sibling("td").string)
            print(Bouwoppervlakte)
            aantal_kamers = (soup.find("td", text="Aantal kamers").find_next_sibling("td").string)
            print(aantal_kamers)
            aantal_slaapkamers = (soup.find("td", text="Aantal slaapkamers").find_next_sibling("td").string)

            # ################
            # #
            # #
            # ################

            r = requests.get(web_url, allow_redirects=True)
            image_name = straatnaam[0].string + ".jpg"
            open(image_name, 'wb').write(r.content)

            # ################
            # #
            # #
            # ################

    if re.search('osonangadjari.com', web_url):
        print(web_url)
        if resp.status_code == 200:
            # ################
            # #
            # #
            # ################
            URL = web_url
            resp = requests.get(URL)
            soup = BeautifulSoup(resp.text, "lxml")

            divs = soup.findAll("table", {"class": "kenmerken"})

            soup = BeautifulSoup(resp.text, "lxml")


            # body > div.page-wrapper > div.main > div > div > div.social-cons > span > a
            postid = soup.select('body > div.page-wrapper > div.main > div > div > div.social-cons > span > a')
            print(postid[0].string)

            straatnaam = soup.select('#post-13962 > h3')
            print(straatnaam[0].string)

            plaats = soup.select('#post-13962 > span')
            print(straatnaam[0].string)


            # Using prijs
            prijs = soup.select('#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(1) > td:nth-child(2)')
            print(prijs[0].text)

            Type = soup.select('#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(2) > td:nth-child(2)')
            print(Type[0].text)

            verkocht = soup.select('#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(3) > td:nth-child(2)')
            print(verkocht[0].text)

            Overeenkomst = soup.select('#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(4) > td:nth-child(2)')
            print(Overeenkomst[0].text)

            Status = soup.select('#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(5) > td:nth-child(2)')
            print(Status[0].text)

            woonoppervlakte = soup.select('#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(6) > td:nth-child(2)')
            print(woonoppervlakte[0].text)

            Perceel_Oppervlakte	 = soup.select('#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(7) > td:nth-child(2)')
            print(Perceel_Oppervlakte[0].text)


            Materiaal = soup.select('#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(8) > td:nth-child(2)')
            print(Materiaal[0].text)


            Aantal_kamers	 = soup.select('#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(9) > td:nth-child(2)')
            print(Aantal_kamers[0].text)


            Slaapkamers = soup.select('#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(10) > td:nth-child(2)')
            print(Slaapkamers[0].text)

            Badkamers = soup.select('#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(11) > td:nth-child(2)')
            print(Badkamers[0].text)

            # ################
            # #
            # #
            # ################


            # property-detail-section-gallery > div > div.property-detail-gallery.owl-carousel.owl-theme.owl-loaded > div.owl-stage-outer.owl-height > div > div.owl-item.active > a > span
            image = soup.select(
                '#property-detail-section-gallery > div > div.property-detail-gallery.owl-carousel.owl-theme.owl-loaded > div.owl-stage-outer.owl-height > div > div.owl-item.active > a > span')



            r = requests.get(image, allow_redirects=True)
            image_name = straatnaam[0].string + ".jpg"
            open(image_name, 'wb').write(r.content)

            # ################
            # #
            # #
            # ################

            print(straatnaam[0].string, type, title, Perceeloppervlakte, Bouwoppervlakte, aantal_kamers,
                  aantal_slaapkamers)
            line = straatnaam[
                       0].string + "," + type + "," + title + "," + Perceeloppervlakte + "," + Bouwoppervlakte + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
            with open('somefile.txt', 'a') as the_file:
                the_file.write(line)



    if re.search('remax.sr', web_url):
        print(web_url)
        if resp.status_code == 200:
            # ################
            # #
            # #
            # ################
            URL = web_url
            resp = requests.get(URL)
            soup = BeautifulSoup(resp.text, "lxml")



            # ################
            # #
            # #
            # ################
            # Using straatnaam
            soup = BeautifulSoup(resp.text, "lxml")
            straatnaam = soup.select('#top_section > h2.title')
            print(straatnaam[0].string)

            # Using prijs
            Vraagprijs = soup.select('#top_section > h2.prijs')
            print(Vraagprijs[0].text)

            Omgeving = soup.select('#top_section > h2.prijs')
            print(Omgeving[0].text)

            Badkamers = soup.select('#top_section > h2.prijs')
            print(Badkamers[0].text)

            Perceelgrootte = soup.select('#top_section > h2.prijs')
            print(Perceelgrootte[0].text)

            Titel = soup.select('#top_section > h2.prijs')
            print(Titel[0].text)

            District = soup.select('#top_section > h2.prijs')
            print(District[0].text)

            Slaapkamers = soup.select('#top_section > h2.prijs')
            print(Slaapkamers[0].text)

            Beschikbaarheid = soup.select('#top_section > h2.prijs')
            print(Beschikbaarheid[0].text)

            Woonoppervlakte = soup.select('#top_section > h2.prijs')
            print(Woonoppervlakte[0].text)


            # ################
            # #
            # #
            # ################

            r = requests.get(web_url, allow_redirects=True)
            image_name = straatnaam[0].string + ".jpg"
            open(image_name, 'wb').write(r.content)

            # ################
            # #
            # #
            # ################


            print(straatnaam[0].string, type, title, Perceeloppervlakte, Bouwoppervlakte, aantal_kamers,
                  aantal_slaapkamers)
            line = straatnaam[
                       0].string + "," + type + "," + title + "," + Perceeloppervlakte + "," + Bouwoppervlakte + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
            with open('somefile.txt', 'a') as the_file:
                the_file.write(line)

    if re.search('affidata.com', web_url):
        print(web_url)
        if resp.status_code == 200:
            # ################
            # #
            # #
            # ################
            URL = web_url
            resp = requests.get(URL)
            soup = BeautifulSoup(resp.text, "lxml")

            divs = soup.findAll("table", {"class": "kenmerken"})

            # ################
            # #
            # #
            # ################
            # Using straatnaam
            soup = BeautifulSoup(resp.text, "lxml")

            titel = soup.select('body > div.container-fluid > div.aff-header > div > div.col-xs-12.col-sm-10 > h4')
            print(titel)

            omschrijving = soup.select('body > div.container-fluid > div.aff-header > div > div.col-xs-12.col-sm-10 > h4')
            print(omschrijving)


            straatnaam = soup.select('#top_section > h2.title')
            print(straatnaam)



            straatnaam = soup.select('body > div.container-fluid > div.aff-header > div > div.col-xs-12.col-sm-10 > h4')
            print(straatnaam)

            # Using prijs
            prijs = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(4) > div.col-xs-12.col-sm-8.nopadding')
            print(prijs)

            plaats = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(5) > div.col-xs-12.col-sm-8.nopadding')
            print(plaats)

            referentienummer = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(6) > div.col-xs-12.col-sm-8.nopadding')
            print(referentienummer)

            views = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(7) > div.col-xs-12.col-sm-8.nopadding')
            print(views)

            woonoppervlak = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(9) > div.col-xs-12.col-sm-8.nopadding')
            print(woonoppervlak)

            verdiepingen = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(10) > div.col-xs-12.col-sm-8.nopadding')
            print(verdiepingen)

            kamers = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(11) > div.col-xs-12.col-sm-8.nopadding')
            print(kamers)

            slaapkamers = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(12) > div.col-xs-12.col-sm-8.nopadding')
            print(slaapkamers)

            badkamers = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(13) > div.col-xs-12.col-sm-8.nopadding')
            print(badkamers)

            toiletten = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(14) > div.col-xs-12.col-sm-8.nopadding')
            print(toiletten)

            nutsvoorzieningen = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(16) > div.col-xs-12.col-sm-8.nopadding')
            print(nutsvoorzieningen)

            tuin = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(18) > div.col-xs-12.col-sm-8.nopadding')
            print(tuin)

            voorzieningen_buiten = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(19) > div.col-xs-12.col-sm-8.nopadding')
            print(voorzieningen_buiten)

            ligging = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(21) > div.col-xs-12.col-sm-8.nopadding')
            print(ligging)

            landschap = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(22) > div.col-xs-12.col-sm-8.nopadding')
            print(landschap)

            vervoer = soup.select('#top_section > h2.prijsbody > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(23) > div.col-xs-12.col-sm-8.nopadding')
            print(vervoer)

            type_woning = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(3) > div.col-xs-12.col-sm-8.nopadding')
            print(type_woning)

            bouwperiode = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(26) > div.col-xs-12.col-sm-8.nopadding')
            print(bouwperiode)

            staat_van_onderhoud = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(27) > div.col-xs-12.col-sm-8.nopadding')
            print(staat_van_onderhoud)

            prijsklasse = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(29) > div.col-xs-12.col-sm-8.nopadding')
            print(prijsklasse)

            bijkomende_kosten = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(30) > div.col-xs-12.col-sm-4.nopadding.text-muted')
            print(bijkomende_kosten)

            perceel = soup.select('body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(31) > div.col-xs-12.col-sm-8.nopadding')
            print(perceel)

            divs = soup.findAll("#banner > div.ns-r4mg9-e-1.row-container > a > canvas")


            # ################
            # #
            # #
            # ################
            # soup = BeautifulSoup(resp.text, "lxml")
            # elements = soup.select('#bottom_section > div > div.kenmerken')
            # print(elements[0])
            # type = (soup.find("td", text="Type").find_next_sibling("td").string)
            # print(type)
            # title = (soup.find("td", text="Titel").find_next_sibling("td").string)
            # print(title)
            # Perceeloppervlakte = (soup.find("td", text="Perceeloppervlakte").find_next_sibling("td").string)
            # print(Perceeloppervlakte)
            # Bouwoppervlakte = (soup.find("td", text="Bouwoppervlakte").find_next_sibling("td").string)
            # print(Bouwoppervlakte)
            # aantal_kamers = (soup.find("td", text="Aantal kamers").find_next_sibling("td").string)
            # print(aantal_kamers)
            # aantal_slaapkamers = (soup.find("td", text="Aantal slaapkamers").find_next_sibling("td").string)
            #
            # divs = soup.findAll("galleria-image")
            # print(divs)
            # divs = soup.findAll("galleria-images")
            # print(divs)
            # divs = soup.findAll("table", {"class": "kenmerken"})
            # print(divs)
            # images = soup.find_all('img')
            # print(images)
            # images_url = images[0]['src']
            # images = soup.findAll('img')
            # for image in images:
            #     print(image['src'])

            # images_url
            # print(images_url)
            # #data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
            # from PIL import Image #pillow library
            # import requests
            # import urllib.request

            # im = Image.open(requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg", stream=True).raw)

            # Opening a new file named img with extension .jpg
            # This file would store the data of the image file
            # f = open('img.jpg', 'wb')
            # # Storing the image data inside the data variable to the file
            # f.write(im)
            # f.close()
            # img_data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
            # with open('netflix.jpg', 'wb') as handler:
            #     handler.write(img_data)
            # with open('pic1.jpg', 'wb') as handle:
            #     response = requests.get('www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg', stream=True)
            #
            #     if not response.ok:
            #         print(response)
            #
            #     for block in response.iter_content(1024):
            #         if not block:
            #             break
            #
            #         handle.write(block)
            # urllib.request.urlretrieve(
            #     'remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg',
            #     "gfg.png")
            #
            # img = Image.open("gfg.png")
            # img.show()

            # find image with '1-' and  followed up with any number that ends with .jpg
            r = requests.get(web_url, allow_redirects=True)
            # image_name = straatnaam[0].string + ".jpg"
            # open(image_name, 'wb').write(r.content)
            # print(straatnaam[0].string, type, title, Perceeloppervlakte, Bouwoppervlakte, aantal_kamers,
            #       aantal_slaapkamers)
            # line = straatnaam[
            #            0].string + "," + type + "," + title + "," + Perceeloppervlakte + "," + Bouwoppervlakte + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
            # with open('somefile.txt', 'a') as the_file:
            #     the_file.write(line)
            #
            # divs = soup.findAll("table", {"class": "kenmerken"})
            # for div in divs:
            #     row = ''
            #     rows = div.findAll('tr')
            #     for row in rows:
            #         print(row)
            #         # if (row.text.find("PHONE") > -1):
            #         #     print(row.text)

    else:
        if re.search('hello.sr|worldeconomics.com|waterkant.com', web_url):
            print(" ")
            #domain = urlparse(web_url).netloc
        else:
            print('Neither url is needed')

    print(web_url)
"""
A function to download the page source of the given URL.
"""
r = requests.get(HOME_PAGE)
source = html.fromstring(r.content)

#source = get_source(HOME_PAGE)
# li_list = source.xpath("//li[contains(@class, 'fpGridBox grid')]")
# item_names = [
#     li.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']") for li in li_list
# ]
#
# # Print news headlines
# elements = dom.xpath("//h3/a[u[@class='StretchedBox']]")
# for elem in elements:
#     print(etree.tostring(elem, method="text", encoding="unicode"))


# ################
# #
# #
# ################


# ################
# #
# #
# ################


# ################
# #
# #
# ################


# ################
# #
# #
# ################

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


#
# class Link(object):
#
#     def __init__(self, src, dst, link_type):
#         self.src = src
#         self.dst = dst
#         self.link_type = link_type
#
#     def __hash__(self):
#         return hash((self.src, self.dst, self.link_type))
#
#     def __eq__(self, other):
#         return (self.src == other.src and
#                 self.dst == other.dst and
#                 self.link_type == other.link_type)
#
#     def __str__(self):
#         return self.src + " -> " + self.dst
#
#
# class Crawler(object):
#
#     def __init__(self, root, depth_limit, confine=None, exclude=[], locked=True, filter_seen=True):
#         self.root = root
#         self.host = urlparse.urlparse(root)[1]
#
#         ## Data for filters:
#         self.depth_limit = depth_limit  # Max depth (number of hops from root)
#         self.locked = locked  # Limit search to a single host?
#         self.confine_prefix = confine  # Limit search to this prefix
#         self.exclude_prefixes = exclude;  # URL prefixes NOT to visit
#
#         self.urls_seen = set()  # Used to avoid putting duplicates in queue
#         self.urls_remembered = set()  # For reporting to user
#         self.visited_links = set()  # Used to avoid re-processing a page
#         self.links_remembered = set()  # For reporting to user
#
#         self.num_links = 0  # Links found (and not excluded by filters)
#         self.num_followed = 0  # Links followed.
#
#         # Pre-visit filters:  Only visit a URL if it passes these tests
#         self.pre_visit_filters = [self._prefix_ok,
#                                   self._exclude_ok,
#                                   self._not_visited,
#                                   self._same_host]
#
#         # Out-url filters: When examining a visited page, only process
#         # links where the target matches these filters.
#         if filter_seen:
#             self.out_url_filters = [self._prefix_ok,
#                                     self._same_host]
#         else:
#             self.out_url_filters = []
#
#     def _pre_visit_url_condense(self, url):
#
#         """ Reduce (condense) URLs into some canonical form before
#         visiting.  All occurrences of equivalent URLs are treated as
#         identical.
#         All this does is strip the \"fragment\" component from URLs,
#         so that http://foo.com/blah.html\#baz becomes
#         http://foo.com/blah.html """
#
#         base, frag = urlparse.urldefrag(url)
#         return base
#
#     ## URL Filtering functions.  These all use information from the
#     ## state of the Crawler to evaluate whether a given URL should be
#     ## used in some context.  Return value of True indicates that the
#     ## URL should be used.
#
#     def _prefix_ok(self, url):
#         """Pass if the URL has the correct prefix, or none is specified"""
#         return (self.confine_prefix is None or
#                 url.startswith(self.confine_prefix))
#
#     def _exclude_ok(self, url):
#         """Pass if the URL does not match any exclude patterns"""
#         prefixes_ok = [not url.startswith(p) for p in self.exclude_prefixes]
#         return all(prefixes_ok)
#
#     def _not_visited(self, url):
#         """Pass if the URL has not already been visited"""
#         return (url not in self.visited_links)
#
#     def _same_host(self, url):
#         """Pass if the URL is on the same host as the root URL"""
#         try:
#             host = urlparse.urlparse(url)[1]
#             return re.match(".*%s" % self.host, host)
#         except Exception, e:
#             print >> sys.stderr, "ERROR: Can't process url '%s' (%s)" % (url, e)
#             return False
#
#     def crawl(self):
#
#         """ Main function in the crawling process.  Core algorithm is:
#         q <- starting page
#         while q not empty:
#            url <- q.get()
#            if url is new and suitable:
#               page <- fetch(url)
#               q.put(urls found in page)
#            else:
#               nothing
#         new and suitable means that we don't re-visit URLs we've seen
#         already fetched, and user-supplied criteria like maximum
#         search depth are checked. """
#
#         q = Queue()
#         q.put((self.root, 0))
#
#         while not q.empty():
#             this_url, depth = q.get()
#
#             # Non-URL-specific filter: Discard anything over depth limit
#             if depth > self.depth_limit:
#                 continue
#
#             # Apply URL-based filters.
#             do_not_follow = [f for f in self.pre_visit_filters if not f(this_url)]
#
#             # Special-case depth 0 (starting URL)
#             if depth == 0 and [] != do_not_follow:
#                 print >> sys.stderr, "Whoops! Starting URL %s rejected by the following filters:", do_not_follow
#
#             # If no filters failed (that is, all passed), process URL
#             if [] == do_not_follow:
#                 try:
#                     self.visited_links.add(this_url)
#                     self.num_followed += 1
#                     page = Fetcher(this_url)
#                     page.fetch()
#                     for link_url in [self._pre_visit_url_condense(l) for l in page.out_links()]:
#                         if link_url not in self.urls_seen:
#                             q.put((link_url, depth + 1))
#                             self.urls_seen.add(link_url)
#
#                         do_not_remember = [f for f in self.out_url_filters if not f(link_url)]
#                         if [] == do_not_remember:
#                             self.num_links += 1
#                             self.urls_remembered.add(link_url)
#                             link = Link(this_url, link_url, "href")
#                             if link not in self.links_remembered:
#                                 self.links_remembered.add(link)
#                 except Exception, e:
#                     print >> sys.stderr, "ERROR: Can't process url '%s' (%s)" % (this_url, e)
#                     # print format_exc()
#
#
# class OpaqueDataException(Exception):
#     def __init__(self, message, mimetype, url):
#         Exception.__init__(self, message)
#         self.mimetype = mimetype
#         self.url = url
#
#
# class Fetcher(object):
#     """The name Fetcher is a slight misnomer: This class retrieves and interprets web pages."""
#
#     def __init__(self, url):
#         self.url = url
#         self.out_urls = []
#
#     def __getitem__(self, x):
#         return self.out_urls[x]
#
#     def out_links(self):
#         return self.out_urls
#
#     # def _addHeaders(self, request):
#     #    request.add_header("User-Agent", AGENT)
#
#     def _open(self):
#         url = self.url
#         try:
#             request = urllib2.Request(url)
#             handle = urllib2.build_opener()
#         except IOError:
#             return None
#         return (request, handle)
#
#     def fetch(self):
#         request, handle = self._open()
#         # self._addHeaders(request)
#         if handle:
#             try:
#                 data = handle.open(request)
#                 mime_type = data.info().gettype()
#                 url = data.geturl();
#                 if mime_type != "text/html":
#                     raise OpaqueDataException("Not interested in files of type %s" % mime_type,
#                                               mime_type, url)
#                 content = unicode(data.read(), "utf-8",
#                                   errors="replace")
#                 soup = BeautifulSoup(content)
#                 tags = soup('a')
#             except urllib2.HTTPError, error:
#                 if error.code == 404:
#                     print >> sys.stderr, "ERROR: %s -> %s" % (error, error.url)
#                 else:
#                     print >> sys.stderr, "ERROR: %s" % error
#                 tags = []
#             except urllib2.URLError, error:
#                 print >> sys.stderr, "ERROR: %s" % error
#                 tags = []
#             except OpaqueDataException, error:
#                 print >> sys.stderr, "Skipping %s, has type %s" % (error.url, error.mimetype)
#                 tags = []
#             for tag in tags:
#                 href = tag.get("href")
#                 if href is not None:
#                     url = urlparse.urljoin(self.url, escape(href))
#                     if url not in self:
#                         self.out_urls.append(url)
#
#
# def getLinks(url):
#     page = Fetcher(url)
#     page.fetch()
#     """for i, url in enumerate(page):
#         print "%d. %s" % (i, url) """
#     j = 1
#     for i, url in enumerate(page):
#         if url.find("http") >= 0:
#             print
#             "%d. %s" % (j, url)
#             j = j + 1
#
#
# def parse_options():
#     """parse_options() -> opts, args
#     Parse any command-line options given returning both
#     the parsed options and arguments.
#     """
#
#     parser = optparse.OptionParser()
#
#     parser.add_option("-q", "--quiet",
#                       action="store_true", default=False, dest="quiet",
#                       help="Enable quiet mode")
#
#     parser.add_option("-l", "--links",
#                       action="store_true", default=False, dest="links",
#                       help="Get links for specified url only")
#
#     parser.add_option("-d", "--depth",
#                       action="store", type="int", default=30, dest="depth_limit",
#                       help="Maximum depth to traverse")
#
#     parser.add_option("-c", "--confine",
#                       action="store", type="string", dest="confine",
#                       help="Confine crawl to specified prefix")
#
#     parser.add_option("-x", "--exclude", action="append", type="string",
#                       dest="exclude", default=[], help="Exclude URLs by prefix")
#
#     parser.add_option("-L", "--show-links", action="store_true", default=False,
#                       dest="out_links", help="Output links found")
#
#     parser.add_option("-u", "--show-urls", action="store_true", default=False,
#                       dest="out_urls", help="Output URLs found")
#
#     parser.add_option("-D", "--dot", action="store_true", default=False,
#                       dest="out_dot", help="Output Graphviz dot file")
#
#     opts, args = parser.parse_args()
#
#     if len(args) < 1:
#         parser.print_help(sys.stderr)
#         raise SystemExit, 1
#
#     if opts.out_links and opts.out_urls:
#         parser.print_help(sys.stderr)
#         parser.error("options -L and -u are mutually exclusive")
#
#     return opts, args
#
#
# class DotWriter:
#     """ Formats a collection of Link objects as a Graphviz (Dot)
#     graph.  Mostly, this means creating a node for each URL with a
#     name which Graphviz will accept, and declaring links between those
#     nodes."""
#
#     def __init__(self):
#         self.node_alias = {}
#
#     def _safe_alias(self, url, silent=False):
#
#         """Translate URLs into unique strings guaranteed to be safe as
#         node names in the Graphviz language.  Currently, that's based
#         on the md5 digest, in hexadecimal."""
#
#         if url in self.node_alias:
#             return self.node_alias[url]
#         else:
#             m = hashlib.md5()
#             m.update(url)
#             name = "N" + m.hexdigest()
#             self.node_alias[url] = name
#             if not silent:
#                 print
#                 "\t%s [label=\"%s\"];" % (name, url)
#             return name
#
#     def asDot(self, links):
#
#         """ Render a collection of Link objects as a Dot graph"""
#
#         print
#         "digraph Crawl {"
#         print
#         "\t edge [K=0.2, len=0.1];"
#         for l in links:
#             print
#             "\t" + self._safe_alias(l.src) + " -> " + self._safe_alias(l.dst) + ";"
#         print
#         "}"
#
#
# def main():
#     opts, args = parse_options()
#
#     url = args[0]
#
#     if opts.links:
#         getLinks(url)
#         raise SystemExit, 0
#
#     depth_limit = opts.depth_limit
#     confine_prefix = opts.confine
#     exclude = opts.exclude
#
#     sTime = time.time()
#
#     print >> sys.stderr, "Crawling %s (Max Depth: %d)" % (url, depth_limit)
#     crawler = Crawler(url, depth_limit, confine_prefix, exclude)
#     crawler.crawl()
#
#     if opts.out_urls:
#         print
#         "\n".join(crawler.urls_seen)
#
#     if opts.out_links:
#         print
#         "\n".join([str(l) for l in crawler.links_remembered])
#
#     if opts.out_dot:
#         d = DotWriter()
#         d.asDot(crawler.links_remembered)
#
#     eTime = time.time()
#     tTime = eTime - sTime
#
#     print >> sys.stderr, "Found:    %d" % crawler.num_links
#     print >> sys.stderr, "Followed: %d" % crawler.num_followed
#     print >> sys.stderr, "Stats:    (%d/s after %0.2fs)" % (
#         int(math.ceil(float(crawler.num_links) / tTime)), tTime)


#
# import asyncio
# import json
# import posixpath
# import re
# from typing import Callable, Dict, List, Optional, Tuple
# from urllib.parse import urljoin, urlparse
#
# from scrapfly import ScrapflyClient, ScrapeConfig, ScrapeApiResponse
# from loguru import logger as log
# from tldextract import tldextract
# from w3lib.url import canonicalize_url
#
#
# class UrlFilter:
#     IGNORED_EXTENSIONS = [
#         # archives
#         '7z', '7zip', 'bz2', 'rar', 'tar', 'tar.gz', 'xz', 'zip',
#         # images
#         'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif', 'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg', 'cdr', 'ico',
#         # audio
#         'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',
#         # video
#         '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv', 'm4a', 'm4v', 'flv', 'webm',
#         # office suites
#         'xls', 'xlsx', 'ppt', 'pptx', 'pps', 'doc', 'docx', 'odt', 'ods', 'odg', 'odp',
#         # other
#         'css', 'pdf', 'exe', 'bin', 'rss', 'dmg', 'iso', 'apk',
#     ]
#
#     def __init__(self, domain=None, subdomain=None, follow=None) -> None:
#         self.domain = domain or ""
#         self.subdomain = subdomain or ""
#         log.info(f"filter created for domain {self.subdomain}.{self.domain}")
#         self.seen = set()
#         self.follow = follow or []
#
#     def is_valid_ext(self, url):
#         """ignore non-crawlable documents"""
#         return posixpath.splitext(urlparse(url).path)[1].lower() not in self.IGNORED_EXTENSIONS
#
#     def is_valid_scheme(self, url):
#         """ignore non http/s links"""
#         return urlparse(url).scheme in ["https", "http"]
#
#     def is_valid_domain(self, url):
#         """ignore offsite urls"""
#         parsed = tldextract.extract(url)
#         return parsed.registered_domain == self.domain and parsed.subdomain == self.subdomain
#
#     def is_valid_path(self, url):
#         """ignore urls of undesired paths"""
#         if not self.follow:
#             return True
#         path = urlparse(url).path
#         for pattern in self.follow:
#             if pattern.match(path):
#                 return True
#         return False
#
#     def is_new(self, url):
#         """ignore visited urls (in canonical form)"""
#         return canonicalize_url(url) not in self.seen
#
#     def filter(self, urls: List[str]) -> List[str]:
#         """filter list of urls"""
#         found = []
#         for url in urls:
#             if not self.is_valid_scheme(url):
#                 log.debug(f"drop ignored scheme {url}")
#                 continue
#             if not self.is_valid_domain(url):
#                 log.debug(f"drop domain missmatch {url}")
#                 continue
#             if not self.is_valid_ext(url):
#                 log.debug(f"drop ignored extension {url}")
#                 continue
#             if not self.is_valid_path(url):
#                 log.debug(f"drop ignored path {url}")
#                 continue
#             if not self.is_new(url):
#                 log.debug(f"drop duplicate {url}")
#                 continue
#             self.seen.add(canonicalize_url(url))
#             found.append(url)
#         return found
#
#
# class Crawler:
#     async def __aenter__(self):
#         self.sesion = ScrapflyClient(
#             key="YOUR_SCRAPFLY_KEY",
#             max_concurrency=2,
#         ).__enter__()
#         return self
#
#     async def __aexit__(self, *args, **kwargs):
#         self.sesion.__exit__(*args, **kwargs)
#
#     def __init__(self, filter: UrlFilter, callbacks: Optional[Dict[str, Callable]] = None) -> None:
#         self.url_filter = filter
#         self.callbacks = callbacks or {}
#
#     def parse(self, results: List[ScrapeApiResponse]) -> List[str]:
#         """find valid urls in responses"""
#         all_unique_urls = set()
#         for result in results:
#             _urls_in_response = set(
#                 urljoin(str(result.context["url"]), url.strip()) for url in result.selector.xpath("//a/@href").getall()
#             )
#             all_unique_urls |= _urls_in_response
#
#         urls_to_follow = self.url_filter.filter(all_unique_urls)
#         # log.info(f"found {len(urls_to_follow)} urls to follow (from total {len(all_unique_urls)})")
#         return urls_to_follow
#
#     async def scrape(self, urls: List[str]) -> Tuple[List[ScrapeApiResponse], List[Exception]]:
#         """scrape urls and return their responses"""
#         log.info(f"scraping {len(urls)} urls")
#
#         to_scrape = [
#             ScrapeConfig(
#                 url=url,
#                 # note: we can enable anti bot protection bypass
#                 # asp=True,
#                 # note: we can also enable rendering of javascript through headless browsers
#                 # render_js=True
#             )
#             for url in urls
#         ]
#         failures = []
#         results = []
#         async for result in self.sesion.concurrent_scrape(to_scrape):
#             if isinstance(result, ScrapeApiResponse):
#                 results.append(result)
#             else:
#                 # some pages might be unavailable: 500 etc.
#                 failures.append(result)
#         return results, failures
#
#     async def run(self, start_urls: List[str], max_depth=10) -> None:
#         """crawl target to maximum depth or until no more urls are found"""
#         url_pool = start_urls
#         depth = 0
#         while url_pool and depth <= max_depth:
#             results, failures = await self.scrape(url_pool)
#             log.info(f"depth {depth}: scraped {len(results)} pages and failed {len(failures)}")
#             url_pool = self.parse(results)
#             await self.callback(results)
#             depth += 1
#
#     async def callback(self, results):
#         for result in results:
#             for pattern, fn in self.callbacks.items():
#                 if pattern.match(result.context["url"]):
#                     fn(result=result)
#
#
# def extract_json_objects(text: str, decoder=json.JSONDecoder()):
#     """Find JSON objects in text, and yield the decoded JSON data"""
#     pos = 0
#     while True:
#         match = text.find("{", pos)
#         if match == -1:
#             break
#         try:
#             result, index = decoder.raw_decode(text[match:])
#             yield result
#             pos = match + index
#         except ValueError:
#             pos = match + 1
#
#
# def find_json_in_script(result: ScrapeApiResponse, keys: List[str]) -> List[Dict]:
#     """find all json objects in HTML <script> tags that contain specified keys"""
#     scripts = result.selector.xpath("//script/text()").getall()
#     objects = []
#     for script in scripts:
#         if not all(f'"{k}"' in script for k in keys):
#             continue
#         objects.extend(extract_json_objects(script))
#     return [obj for obj in objects if all(k in str(obj) for k in keys)]
#
#
# results = []
#
#
# def parse_product(result: ScrapeApiResponse):
#     products = find_json_in_script(result, ["published_at", "price"])
#     results.extend(products)
#     if not products:
#         log.warning(f"could not find product data in {result}")
#
#
# async def run():
#     callbacks = {re.compile(".+/products/.+"): parse_product}
#     url_filter = UrlFilter(domain="nytimes.com", subdomain="store")
#     async with Crawler(url_filter, callbacks=callbacks) as crawler:
#         await crawler.run(['https://store.nytimes.com/'])
#     print(results)


# if __name__ == "__main__":
#     asyncio.run(run())


#
# class AliexpressTabletsSpider(scrapy.Spider):
#     name = 'aliexpress_tablets'
#     allowed_domains = ['aliexpress.com']
#     start_urls = ['https://www.aliexpress.com/category/200216607/tablets.html']
#
#
#     custom_settings={ 'FEED_URI': "aliexpress_%(time)s.csv",
#                        'FEED_FORMAT': 'csv'}
#
#     def parse(self, response):
#
#         print("procesing:"+response.url)
#         #Extract data using css selectors
#         product_name=response.css('.product::text').extract()
#         price_range=response.css('.value::text').extract()
#         #Extract data using xpath
#         orders=response.xpath("//em[@title='Total Orders']/text()").extract()
#         company_name=response.xpath("//a[@class='store $p4pLog']/text()").extract()
#
#         row_data=zip(product_name,price_range,orders,company_name)
#
#         #Making extracted data row wise
#         for item in row_data:
#             #create a dictionary to store the scraped info
#             scraped_info = {
#                 #key:value
#                 'page':response.url,
#                 'product_name' : item[0], #item[0] means product in the list and so on, index tells what value to assign
#                 'price_range' : item[1],
#                 'orders' : item[2],
#                 'company_name' : item[3],
#             }
#
#             #yield or give the scraped info to scrapy
#             yield scraped_info
#
#
#             NEXT_PAGE_SELECTOR = '.ui-pagination-active + a::attr(href)'
#             next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
#             if next_page:
#                 yield scrapy.Request(
#                 response.urljoin(next_page),
#                 callback=self.parse)
#
# with Controller.from_port(port=9051) as controller:
#     # Set the controller password
#     controller.authenticate(password='mypassword')
#
#     # Set the starting URL
#     url = 'http://example.com'
#
#     # Initialize the visited set and the link queue
#     visited = set()
#     queue = [url]
#
#     # Get the list of keywords to search for
#     keywords = input('Enter a list of keywords to search for, separated by commas: ').split(',')
#
#     # Crawl the links
#     while queue:
#         # Get the next link in the queue
#         link = queue.pop(0)
#
#         # Skip the link if it has already been visited
#         if link in visited:
#             continue
#
#         # Set the new IP address
#         controller.signal(Signal.NEWNYM)
#
#         # Send the request to the URL
#         response = requests.get(link, headers=headers)
#
#         # Parse the response
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # Find all links on the page
#         links = soup.find_all('a')
#
#         # Add any links that contain the keywords to the queue
#         for a in links:
#             href = a.get('href')
#             if any(keyword in href for keyword in keywords):
#                 queue.append(href)
#
#         # Add the link to the visited set
#         visited.add(link)
#
#         # Print the title and URL of the page
#         print(soup.title.string, link)
#
#         # Check if the number of visited links has reached the limit
#         if len(visited) >= num_links_to_crawl:
#             break
#
# def print_visited_links():
#     # Print the visited links
#     print('Visited links:')
#     for link in visited:
#         print(link)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
