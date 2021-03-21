import pandas as pd
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
from googlesearch import search
import time
import xml.etree.ElementTree as ET
import awis


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

    def aws_query(self):
        myfile = open('urls_data.txt', 'w')
        for i, row in self.data.iterrows():
            if i >= 120 and i < 160:
                url = row['Url1']
                print(url)
                data = awis.run(url)
                rez = self.parse(data)
                rez = ' '.join(map(str,rez))
                myfile.write("%s\n" % rez)

        myfile.close()

    def parse(self, data):
        myroot = ET.fromstring(data)
        td = myroot[1][0][0].find('TrafficData')
        rank_overall = td.find('Rank').text

        try:
            reach = myroot[1][0][0][1][2][0].find('Reach')
            reach_rank = reach.find('Rank').find('Value').text
            reach_permil = reach.find('PerMillion').find('Value').text
        except IndexError:
            reach_rank, reach_permil = -1, -1

        try:
            pv = myroot[1][0][0][1][2][0].find('PageViews')
            pv_rank = pv.find('Rank').find('Value').text
            pv_peruser = pv.find('PerUser').find('Value').text
        except IndexError:
            pv_rank, pv_peruser = -1, -1

        print(' '.join(map(str,[rank_overall, reach_rank, reach_permil, pv_rank, pv_peruser])))
        return [rank_overall, reach_rank, reach_permil, pv_rank, pv_peruser]


if __name__ == '__main__':
    df_result = pd.read_excel(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\merged_companies.xlsx')
    #obj = UrlQuery(df_result)
    #df_result = obj.create_urls()
    #df_result.to_excel(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\merged_companies.xlsx')

    obj1 = WebStatQuery(df_result)
    obj1.aws_query()


