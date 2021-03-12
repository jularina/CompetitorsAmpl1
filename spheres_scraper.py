from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import re
import numpy as np


# --| Setup

class SpheresLasers:
    def __init__(self):
        self.options = Options()
        self.define_options()
        self.browser = webdriver.Chrome(
            executable_path=r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe',
            options=self.options)
        self.url = 'https://www.laserdiodesource.com/'
        self.classname = "colSpecImage"
        self.df_companies = pd.DataFrame(columns=['Company', 'Description', 'Wavelength', 'Energy', 'Price', 'Shipment'])

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
        dfs = []

        for url_inside in links:
            browser2 = webdriver.Chrome(
                executable_path=r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe',
                options=self.options)
            browser2.get(url_inside)
            df_result = self.view_sphere(browser2, url_inside)
            dfs.append(df_result)

        df_res = dfs[0].merge(dfs[1], left_on='Company', right_on='Company', how='outer')
        return df_res

    def view_sphere(self, br, url_inside):
        n = len(br.find_element_by_xpath('//*[@id="sidebar"]/div[2]/section[9]/nav/ul').text.splitlines())
        dfs = []
        for i in range(1, n+1):
            browser3 = webdriver.Chrome(
                executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
                options=self.options)
            browser3.get(url_inside)
            browser3.find_element_by_xpath('//*[@id="sidebar"]/div[2]/section[9]/nav/ul/li['+str(1)+']/input').click()
            time.sleep(10)
            companies = self.spheres_get(browser3)
            df = pd.DataFrame(index=companies)
            df[i] = 1
            dfs.append(df)
        df_result = dfs[0].merge(dfs[1], left_on='Company', right_on='Company', how='outer')
        return df_result

    def spheres_get(self, br):
        nums = len(br.find_elements_by_class_name(self.classname))
        companies = []
        for i in range(1, nums + 1):
            arr = br.find_element_by_xpath('//*[@id="sProductList"]/li[' + str(i) + ']/span[1]/a').text.splitlines()
            companies.append(arr[-1])

        return companies

    def run(self):
        self.connection()
        df_res = self.info_get()
        return df_res


if __name__ == '__main__':
    parsed_sphere_lasers = SpheresLasers()
    df_companies_diodes = parsed_sphere_lasers.run()
    df_companies_diodes.to_csv(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_spheres.csv')