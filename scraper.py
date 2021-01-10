import requests
from bs4 import BeautifulSoup
import lxml

url = 'https://spie.org/ExhibitorDatabase/Search'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

print(soup)