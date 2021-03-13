from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import pandas as pd
from functools import reduce


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
        cells = [9, 11, 14, 14, 7, 12, 8, 8, 8]
        for url_inside, cell in zip(links, cells):
            browser2 = webdriver.Chrome(
                executable_path=r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe',
                options=self.options)
            browser2.get(url_inside)
            df_result = self.view_sphere(browser2, url_inside, cell)
            dfs.append(df_result)

        df_res = reduce(lambda df1, df2: df1.merge(df2, "outer", left_on='Company', right_on='Company'), dfs)
        df_res.drop_duplicates(inplace=True)
        return df_res

    def view_sphere(self, br, url_inside, cell):
        arr = br.find_elements_by_xpath("//*[@id='sidebar']/div[2]/section["+str(cell)+"]/nav/ul/li")
        n = len(arr)
        dfs = []
        for i in range(1, n+1):
            browser3 = webdriver.Chrome(
                executable_path=r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe',
                options=self.options)
            browser3.get(url_inside)
            browser3.find_element_by_xpath('//*[@id="sidebar"]/div[2]/section['+str(cell)+']/nav/ul/li['+str(i)+']/input').click()
            time.sleep(10)
            companies = self.spheres_get(browser3)
            df = pd.DataFrame(index=companies)
            df['Company'] = companies
            df[arr[i-1].text] = 1
            dfs.append(df)
            print(arr[i-1].text, df.shape)
        df_result = reduce(lambda df1, df2: df1.merge(df2, "outer", left_on='Company', right_on='Company'), dfs)
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