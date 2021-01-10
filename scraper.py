import requests
from bs4 import BeautifulSoup
import lxml

url = input('Enter url: ')
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
tags = soup('a')

for tag in tags:
    print(tag.get('href', None))