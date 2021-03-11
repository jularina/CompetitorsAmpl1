from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


# --| Setup

class ParserDiodes:
    def __init__(self):
        self.options = Options()
        self.define_options()
        self.browser = webdriver.Chrome(
            executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
            options=self.options)
        self.url = 'https://www.laserdiodesource.com/'
        self.classname = "colSpecImage"
        self.df_companies = pd.DataFrame(columns=['Company', 'Description', 'Wavelength', 'Energy', 'Price'])

    def define_options(self):
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=1980,1020")
        self.options.add_argument('--no-sandbox')

    def connection(self):
        self.browser.get(self.url)
        time.sleep(2)

    def info_get(self):
        links_obj = self.browser.find_elements_by_link_text('view all data sheets & manufacturers')
        links = [link.get_attribute('href') for link in links_obj]

        for url in links:
            browser2 = webdriver.Chrome(
                executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
                options=self.options)
            browser2.get(url)
            self.view_all(browser2)

    def view_all(self, br):
        nums = len(br.find_elements_by_class_name(self.classname))

        for i in range(1, nums + 1):
            arr = br.find_element_by_xpath('//*[@id="sProductList"]/li[' + str(i) + ']/span[1]/a').text.splitlines()
            arr1 = br.find_element_by_xpath('//*[@id="sProductList"]/li[' + str(i) + ']/span[2]').text.splitlines()
            price = None if not arr1 else arr1[0]
            self.df_companies = self.df_companies.append(
                {'Company': arr[-1], 'Description': ' '.join(arr[2:-1]), 'Wavelength': arr[0], 'Energy': arr[1],
                 'Price': price}, ignore_index=True)

    def run(self):
        self.connection()
        self.info_get()
        return self.df_companies


if __name__ == '__main__':
    parserdiodes = ParserDiodes()
    df_companies_diodes = parserdiodes.run()
    df_companies_diodes.to_csv(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_diodes.csv')
