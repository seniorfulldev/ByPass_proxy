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

# Example list of urls to scrape
list_of_urls = [
    'https://www.sportsmansguide.com/productlist?k=glock%2043',
    'https://www.sportsmansguide.com/productlist?k=Beretta%20M9',
]

scraped_quotes = []

def scrape_url(url):
    print(urllib.parse.urlparse(url).query)
    query = urllib.parse.urlparse(url).query
    title_query = query.split('=')[1]
    kquery = title_query
    if '%20' in title_query:
        key = '%20'
        kquery = title_query.replace(key, '_')
        print(kquery)
    response = client.get(url=url, retry=NUM_RETRIES)

    # parse data if 200 status code (successful response)
    if response.status_code == 200:
        # Example: parse data with beautifulsoup
        html_response = response.text
        soup = BeautifulSoup(html_response, "html.parser")
        quotes_sections = soup.find_all('div', class_="product-tile")

        # loop through each quotes section and extract the quote and author
        for quote_block in quotes_sections:
            if(quote_block.find('img', class_='product') is None):
                continue
            title = quote_block.find('h2').text
            if(quote_block.find('p', class_='sold-out') is None):
                price = quote_block.find('span', class_='price').text
            else:    
                price = quote_block.find('p', class_='sold-out').text
            if(quote_block.find('span', class_='rating-count') is None):
                rating = "No Given Review"
            else:    
                rating = quote_block.find('span', class_='rating-count').text
            if(quote_block.find('img', class_='product').get('data-src') is None):
                image = quote_block.find('img', class_='product')['src']
            else:
                image = quote_block.find('img', class_='product').get('data-src')

            # add scraped data to "scraped_quotes" list
            scraped_quotes.append({
                'image': image,
                'title': title,
                'rating': rating,
                'price': price
            })
            with open('./data/{}.csv'.format(kquery), mode='a') as f:
                result_writer = csv.writer(
                    f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                result_writer.writerow([image, title, price, rating])
    else:
        print(response.status_code)

with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    executor.map(scrape_url, list_of_urls)