import cloudscraper
import requests
import urllib3, socket
scraper = cloudscraper.create_scraper()
# print (requests.get("https://linktracker.pro").content)

print(scraper.get("https://linktracker.pro", proxies={'https': 'http://45.55.46.222:8080'}, headers={
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}).content)
