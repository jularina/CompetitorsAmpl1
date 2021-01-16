from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


# --| Setup

class Parserlasers:
    def __init__(self):
        self.options = Options()
        self.define_options()
        self.browser = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
                               options=self.options)
        self.df_companies = pd.DataFrame(columns=['Company', 'Description', 'Wavelength', 'Energy'])

    def define_options(self):
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=1980,1020")
        self.options.add_argument('--no-sandbox')

    def connection(self):
        self.browser.get(self.url)
        time.sleep(2)

    def view_all(self):
        nums = len(self.browser.find_elements_by_class_name(self.classname))
        for i in range(1, nums + 1):
            arr = self.browser.find_element_by_xpath('//*[@id="sProductList"]/li[' + str(i) + ']/span[1]/a').text.splitlines()
            self.df_companies.loc[i-1] = [arr[3], arr[2], arr[0], arr[1]]

    def run(self):
        self.connection()
        self.view_all()
        return self.df_companies


class Parserpics(Parserlasers):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.laserlabsource.com/Solid-State-Lasers/Picosecond-Pulse-Lasers'
        self.classname = "nColPicosecond_Pulse_Lasers_wavelength"


class Parserfems(Parserlasers):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.laserlabsource.com/Solid-State-Lasers/Femtosecond-Pulse-Lasers'
        self.classname = "nColFemtosecond_Pulse_Lasers_wavelength"


if __name__ == '__main__':
    parserpics = Parserpics()
    df_companies_pics = parserpics.run()
    df_companies_pics.to_csv(r'C:\Users\Arina27\Desktop\Arina\diplom\data\parsing\parsed_picosecond.csv')

    parserfems = Parserfems()
    df_companies_fems = parserfems.run()
    df_companies_fems.to_csv(r'C:\Users\Arina27\Desktop\Arina\diplom\data\parsing\parsed_femtosecond.csv')
