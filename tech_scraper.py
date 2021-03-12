from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


class TechnologyLasers:
    def __init__(self):
        self.options = Options()
        self.define_options()
        self.browser = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe',
                               options=self.options)
        self.df_companies = pd.DataFrame(columns=['Company', 'Technologies'])

    def define_options(self):
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=1980,1020")
        self.options.add_argument('--no-sandbox')

    def connection(self):
        self.browser.get(self.url)
        time.sleep(2)

    def view_tech(self):
        n = len(self.browser.find_element_by_xpath("//*[@id='sidebar']/div[2]/section[4]/nav/ul").text.splitlines())
        dfs = []
        for i in range(1, n+1):
            browser2 = webdriver.Chrome(
                executable_path=r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe',
                options=self.options)
            browser2.get(self.url)
            browser2.find_element_by_xpath('//*[@id="sidebar"]/div[2]/section[4]/nav/ul/li['+str(i)+']/input').click()
            time.sleep(10)
            companies = self.technologies_get(browser2)
            df = pd.DataFrame(index=companies)
            df[i] = 1
            dfs.append(df)
        df_result = dfs[0].merge(dfs[1], left_on='Company', right_on='Company', how='outer')
        return df_result

    def technologies_get(self, br):
        nums = len(br.find_elements_by_class_name(self.classname))
        companies = []
        for i in range(1, nums + 1):
            arr = br.find_element_by_xpath('//*[@id="sProductList"]/li[' + str(i) + ']/span[1]/a').text.splitlines()
            companies.append(arr[-1])

        return companies

    def run(self):
        self.connection()
        df_result = self.view_tech()
        return df_result


class ParserTechPics(TechnologyLasers):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.laserlabsource.com/Solid-State-Lasers/Picosecond-Pulse-Lasers'
        self.classname = "nColPicosecond_Pulse_Lasers_wavelength"


class ParserTechFems(TechnologyLasers):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.laserlabsource.com/Solid-State-Lasers/Femtosecond-Pulse-Lasers'
        self.classname = "nColFemtosecond_Pulse_Lasers_wavelength"


if __name__ == '__main__':
    parser_tech_pics = ParserTechPics()
    dftech_companies_pics = parser_tech_pics.run()
    dftech_companies_pics.to_csv(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_technologies.csv')

    parser_tech_fems = ParserTechFems()
    dftech_companies_fems = parser_tech_fems.run()
    dftech_companies_fems.to_csv(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_technologies.csv')
