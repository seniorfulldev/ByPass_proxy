from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

browser = webdriver.Firefox()
browser.get("url")
delay = 3  # seconds
try:
    myElem = WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
