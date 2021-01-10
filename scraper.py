import requests
from selenium import webdriver
from bs4 import BeautifulSoup

#url = input('Enter url: ')
url = 'https://spie.org/ExhibitorDatabase/Search?SSO=1'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# for link in soup.find_all('a'):
#     print('*************')
#     print(link)
#     print(link.get('href'))

driver = webdriver.Chrome('C:/Users/Arina27/Downloads/chromedriver.exe')
driver.get(url)
page = driver.page_source
# page = driver.execute_script('return document.body.innerHTML')
soup = BeautifulSoup(page, 'html.parser')

for link in soup.find_all('a'):
    print('*************')
    print(link)
    print(link.get('href'))