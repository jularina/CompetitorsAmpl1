from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

# --| Setup
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1980,1020")
browser = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options=options)

url = 'https://spie.org/ExhibitorDatabase/Search?SSO=1'
browser.get(url)
time.sleep(2)

tags = browser.find_elements_by_class_name('formLink01')
tags = tags[5::4][:10]

for tag in tags:
    url2 = browser.find_element_by_link_text(tag.text).get_attribute('href')
    browser2 = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
                                options=options)
    browser2.get(url2)
    try:
        description = browser2.find_element_by_id('Main_lblCompanyDescription').text
        link = browser2.find_elements_by_class_name('formText07')

    except NoSuchElementException:
        description = 'No description'
        link = 'No link'

    print('Company name: ', tag.text, '\n', 'Company description: ', description, '\n')

    if isinstance(link, str):
        print(link)
    else:
        print('Address: ', link[2].text.splitlines()[1:], '\n')
        print('Website: ', link[3].text[9:])