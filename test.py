from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# --| Setup
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1980,1020")
browser = webdriver.Chrome(executable_path='C:/Users/Arina27/Downloads/chromedriver.exe', options=options)

url = 'https://spie.org/ExhibitorDatabase/Search?SSO=1'
browser.get(url)
time.sleep(2)

tags = browser.find_elements_by_class_name('formLink01')

for tag in tags:
    print(tag.text)
