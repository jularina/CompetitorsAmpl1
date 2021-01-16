from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


# --| Setup

class Parser:
    def __init__(self):
        self.options = Options()
        self.define_options()
        self.browser = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
                               options=self.options)
        self.df_companies = pd.DataFrame(columns=['Company', 'Description', 'Address', 'Website'])

    def define_options(self):
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=1980,1020")
        self.options.add_argument('--no-sandbox')

    def connection(self):
        url = 'https://spie.org/ExhibitorDatabase/Search?SSO=1'
        self.browser.get(url)
        time.sleep(2)

    def view_all(self):
        self.browser.find_element_by_xpath("//*[@id='lnkViewAll']").click()
        time.sleep(10)

    def find_companies(self):
        tags = self.browser.find_elements_by_class_name('formLink01')
        tags = tags[5:]
        tags = [tag.text for tag in tags]
        tags = list(filter(None, tags))
        tags = list(filter(lambda k: '+ Add' not in k, tags))

        for i, tag in enumerate(tags):
            self.info_get(i=i, tag=tag)

    def info_get(self, i: int, tag):
        url2 = self.browser.find_element_by_link_text(tag).get_attribute('href')
        browser2 = webdriver.Chrome(
            executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
            options=self.options)
        browser2.get(url2)
        try:
            description = browser2.find_element_by_id('Main_lblCompanyDescription').text
            address = browser2.find_elements_by_class_name('formText07')
            link = browser2.find_element_by_partial_link_text('www.').text

        except NoSuchElementException:
            description = 'No description'
            link, address_new = 'No link', 'No address'

        if link != 'No link':
            address_list = []
            for addr in address[1:]:
                if 'Booth' in addr.text:
                    continue
                elif 'Website' in addr.text:
                    break
                else:
                    var = addr.text
                    var = var[var.index('\n') + 1:]
                    address_list.append(var)

            address_new = address_list[0].replace('\n', ' ')

        self.df_companies.loc[i] = [tag, description, address_new, link]

    def run(self):
        self.connection()
        self.view_all()
        self.find_companies()
        return self.df_companies


if __name__ == '__main__':
    parser = Parser()
    df_companies = parser.run()
    df_companies.to_csv(r'C:\Users\Arina27\Desktop\Arina\diplom\data\parsing\parsed_companies1.csv')
