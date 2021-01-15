import requests
from bs4 import BeautifulSoup

blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'style']
url = "https://www.acphotonics.com"

html = requests.get(url).content
soup = BeautifulSoup(html, "html.parser")

# Keep only 'href' from front page.
links = [a["href"] for a in soup.find_all("a", href=True)]
links = set(links).add(url)

# Get text from all links
text = soup.find_all(text=True)