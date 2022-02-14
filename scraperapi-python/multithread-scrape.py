from os import times, urandom
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import sys
import csv
import concurrent.futures
import threading
import time
MAX_THREADS = 20


def extract_movie_details(movie_link):
    # times.sleep(urandom.uniform(0, 0.2))
    movie_soup = BeautifulSoup(requests.get(movie_link).text, 'lxml')
    # print(movie_soup)
    title = movie_soup.find(
        "span", attrs={"data-testid": "title"}).get_text()

    rating = movie_soup.find("span", attrs={"class": "ipc-rating-star--imdb"}).get_text(
    ) if movie_soup.find("span", attrs={"class": "ipc-rating-star--imdb"}) else None

    print(title, rating)

    with open('./data/result.csv', mode='a') as f:
        movie_writer = csv.writer(
            f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        movie_writer.writerow([title, rating])


def extract_movies(soup):
    movies_table = soup.find(
        "table", attrs={"data-caller-name": "chart-moviemeter"}).find("tbody")
    movies_tablerows = movies_table.find_all("tr")
    movie_links = ["https://imdb.com" +
                   movie.find("a")["href"] for movie in movies_tablerows]

    # for movie_link in movie_links:
    #     print(movie_link)
    #     extract_movie_details(movie_link)
    threads = min(MAX_THREADS, len(movie_links))  # no. of threads to use
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(extract_movie_details, movie_links)


def main():
    start = time.time()
    print(start)
    # start_time = times.time()
    # IMDB Most Popular Movies - 100 movies
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    r = requests.get(popular_movies_url)
    # soup = bs(r.content)
    soup = BeautifulSoup(r.text, 'lxml')

    # Main function to extract the 100 movies from IMDB Most Popular Movies
    extract_movies(soup)

    # end_time = times.time()
    # print("Total time taken: ", end_time-start_time)
    end = time.time()
    print("Total time taken: ", end - start)


main()
