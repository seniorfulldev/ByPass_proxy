from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import urllib.parse
import json
import csv
import requests.exceptions
import time

API_KEY = 'a746f647646b410e486e00da3b11f453'
NUM_RETRIES = 2

# we will store the scraped data in this list
scraped_quotes = []

# urls to scrape
url_list = [
    'https://www.sportsmansguide.com/productlist?k=glock%2043',
    'https://www.sportsmansguide.com/productlist?k=Beretta%20M9',
]


def get_scraperapi_url(url):
    """
        Converts url into API request for Scraper API.
    """
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


def status_code_first_request(performance_log):
    """
        Selenium makes it hard to get the status code of each request,
        so this function takes the Selenium performance logs as an input
        and returns the status code of the first response.
    """
    for line in performance_log:
        try:
            json_log = json.loads(line['message'])
            print(json_log)
            if json_log['message']['method'] == 'Network.responseReceived':
                return json_log['message']['params']['response']['status']
        except:
            pass
    return json.loads(response_recieved[0]['message'])['message']['params']['response']['status']


# optional --> define Selenium options
option = webdriver.ChromeOptions()
option.add_argument('--headless')  # --> comment out to see the browser launch.
option.add_argument('--no-sandbox')
option.add_argument('--log-level=3')
option.add_argument('--disable-dev-sh-usage')

# enable Selenium logging
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}


# set up Selenium Chrome driver
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=option, desired_capabilities=caps)
for url in url_list:
    query = urllib.parse.urlparse(url).query
    title_query = query.split('=')[1]
    kquery = title_query
    if '%20' in title_query:
        key = '%20'
        kquery = title_query.replace(key, '_')
    for _ in range(NUM_RETRIES):
        try:
            driver.get(get_scraperapi_url(url))
            print("start")
            time.sleep(25)
            print("delay")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            performance_log = driver.get_log('performance')
            status_code = status_code_first_request(performance_log)
            if status_code in [200, 404]:
                # escape for loop if the API returns a successful response
                break
        except requests.exceptions.ConnectionError:
            driver.close()

    if status_code == 200:
        # feed HTML response into BeautifulSoup
        html_response = driver.page_source
        soup = BeautifulSoup(html_response, "html.parser")

        # find all quotes sections
        quotes_sections = soup.find_all('div', class_="product-tile")
        # for item in soup.findAll("img", class_="lazy"):
        #     print(item.get("data-lazy"))
        # loop through each quotes section and extract the quote and author
        for quote_block in quotes_sections:
            if(quote_block.find('img', class_='product') is None):
                image = "test image"
                title = "test title"
            else:
                image = quote_block.find('img', class_='product')['src']
                title = quote_block.find('h2').text
                print("image", image);
            # image = quote_block.find('img', class_='product')['src']

            scraped_quotes.append({
                'image': image,
                'title': title
            })
            with open('./data/{}.csv'.format(kquery), mode='a') as f:
                result_writer = csv.writer(
                    f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                result_writer.writerow([image, title])


print(scraped_quotes)
