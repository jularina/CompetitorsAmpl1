import pandas as pd
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
from googlesearch import search
import time


# Google url search
class UrlQuery:
    def __init__(self, df):
        self.data = df
        self.urls1, self.urls2 = [], []
        self.FIFTEEN_MINUTES = 900
        self.queries = self.data['Company'].values

    # @on_exception(expo, RateLimitException, max_tries=8)
    # @limits(calls=15, period=self.FIFTEEN_MINUTES)
    def call_api(self, q):
        urls = search(q + ' lasers', tld='co.in', num=2, stop=2, pause=10)
        url1 = next(iter(urls))
        url2 = next(iter(urls))
        self.urls1.append(url1)
        self.urls2.append(url2)
        print(url1)

    def create_urls(self):
        for query in self.queries:
            time.sleep(15)
            self.call_api(query)

        self.data['Url1'] = self.urls1
        self.data['Url2'] = self.urls2

        return self.data


class WebStatQuery:
    def __init__(self, df):
        self.data = df
        self.API_KEY = 'rHoyz0awCN5NXG7udWyBj62iBQNhbaUh7XqbQjHB'


if __name__ == '__main__':
    df_result = pd.read_excel(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\merged_companies.xlsx')
    obj = UrlQuery(df_result)
    df_result = obj.create_urls()
    df_result.to_excel(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\merged_companies.xlsx')


