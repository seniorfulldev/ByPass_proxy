from bs4 import BeautifulSoup
import concurrent.futures
import csv
import urllib.parse
from scraper_api import ScraperAPIClient


"""
SCRAPER SETTINGS
You need to define the following values below:
- API_KEY --> Find this on your dashboard url: https://dashboard.scraperapi.com/dashboard
                
- NUM_THREADS --> Set this equal to the number of concurrent threads available
                in your scraperapi plan.
"""
API_KEY = 'd3ac880a20ac99c18859cfac13de7a03'
NUM_RETRIES = 3
NUM_THREADS = 10

client = ScraperAPIClient(API_KEY)

# Example list of ammos to scrape
list_of_ammos = [
    '223-Remington',
    '8mm-lebel-revolver',
]

scraped_quotes = []

def scrape_url(seo_name):
    response = client.post(url = 'https://ammoseek.com/', body = {'draw': 1,'seo_name': seo_name ,'search_ammo': '1','start': '0', 'length': '100' }, retry=3, timeout=60)

    # parse data if 200 status code (successful response)
    if response.status_code == 200:
        print(type(response.json()))
        print(response.json()['data'])
    else:
        print("status_code______", response.status_code)

with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    executor.map(scrape_url, list_of_ammos)
