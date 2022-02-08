import cloudscraper

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
print(scraper.get("https://www.sportsmansguide.com/productlist?k=glock%2043").text)  # => "<!DOCTYPE html><html><head>..."