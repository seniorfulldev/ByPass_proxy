# from bs4 import BeautifulSoup
# import concurrent.futures
# import csv
# import urllib.parse
from scraper_api import ScraperAPIClient

API_KEY = 'a746f647646b410e486e00da3b11f453'
client = ScraperAPIClient(API_KEY)

postResult = client.post(url = 'https://ammoseek.com/', body = {'seo_name': '223-Remington','search_ammo': '1'}).text
  
print(postResult)
