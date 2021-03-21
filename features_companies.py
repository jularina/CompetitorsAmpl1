import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from apis_queries import UrlQuery, WebStatQuery


class GroupMaking:
    def __init__(self):
        self.diodes_companies = pd.read_csv(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing'
                                            r'\parsed_diodes.csv',
                                            index_col='Unnamed: 0')
        self.pics_companies = pd.read_csv(
            r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_picosecond.csv',
            index_col='Unnamed: 0')
        self.fems_companies = pd.read_csv(
            r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_femtosecond.csv',
            index_col='Unnamed: 0')
        self.tech_companies = pd.read_csv(
            r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_technologies.csv',
            index_col='Unnamed: 0')
        self.sphere_companies = pd.read_csv(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing'
                                            r'\parsed_spheres.csv',
                                            index_col='Unnamed: 0')
        self.tech_sphere_comps = self.merge_spheres_tech()

    def merge_spheres_tech(self):
        tech_list, sphere_list = list(self.tech_companies.columns)[1:], list(self.sphere_companies.columns)[1:]
        medical_list = [i for i in sphere_list if 'medical / aesthetics' in i]

        self.tech_companies['Total'] = self.tech_companies[tech_list].sum(axis=1)
        self.sphere_companies['Total'] = self.sphere_companies[sphere_list].sum(axis=1)
        self.sphere_companies['Total_medicine'] = self.sphere_companies[medical_list].sum(axis=1)
        self.sphere_companies['Total_medicine'] = np.where(self.sphere_companies['Total_medicine'] >= 1.0, 1.0, 0.0)
        self.tech_companies.drop(tech_list, axis=1, inplace=True)
        self.sphere_companies.drop(sphere_list, axis=1, inplace=True)

        return self.tech_companies.merge(self.sphere_companies, left_on='Company', right_on='Company', how='outer')

    def merge_products(self):
        self.diodes_companies = self.diodes_companies.drop_duplicates()[
            ['Company', 'Wavelength', 'Energy', 'Price', 'Shipment']]
        self.pics_companies = self.pics_companies.drop_duplicates()[['Company', 'Wavelength', 'Energy']]
        self.fems_companies = self.fems_companies.drop_duplicates()[['Company', 'Wavelength', 'Energy']]
        self.diodes_companies['Price'] = self.diodes_companies['Price'].str.slice(start=1).str.replace(',', '')
        self.diodes_companies['Price'] = self.diodes_companies['Price'].astype(float)
        self.diodes_companies['Shipment'] = self.diodes_companies['Shipment'].astype(float)

        cols = ['Wavelength', 'Energy']
        dfs = [self.diodes_companies, self.pics_companies, self.fems_companies]
        for df in dfs:
            df.replace({'  —': np.NaN}, inplace=True)
            for col in cols:
                df[col] = df[col].str.split().str[0]
                df[col] = df[col].astype(float)
            df.fillna(value=df.quantile(q=0.25), inplace=True)

        self.pics_companies.rename(columns={'Wavelength': 'Wavelength_p', 'Energy': 'Energy_p'}, inplace=True)
        self.fems_companies.rename(columns={'Wavelength': 'Wavelength_f', 'Energy': 'Energy_f'}, inplace=True)
        pics_companies = self.pics_companies.groupby(by=["Company"]).median().reset_index()
        fems_companies = self.fems_companies.groupby(by=["Company"]).median().reset_index()
        diodes_companies = self.diodes_companies.groupby(by=["Company"]).median().reset_index()

        df_result = pics_companies.merge(fems_companies, left_on='Company', right_on='Company', how='outer')
        df_result = df_result.merge(diodes_companies, left_on='Company', right_on='Company', how='outer')
        df_result = df_result.merge(self.tech_sphere_comps, left_on='Company', right_on='Company', how='outer')
        df_result = self.ransform_result(df_result)

        return df_result

    def transform_result(self, df):
        df['Price'].fillna(df['Price'].mean(), inplace=True)
        df['Shipment'].fillna(df['Shipment'].mean(), inplace=True)
        df['Shipment'] = df['Shipment'] * 7
        df.fillna(0, inplace=True)


class ConferenceMembership:
    def __init__(self, df):
        self.spie_companies = pd.read_csv(
            r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_companies.csv',
            index_col='Unnamed: 0')
        self.df_result = df

    def find_similar_companies(self):
        mp_comps = list(self.df_result['Company'])
        spie_comps = list(set(self.spie_companies['Company']))
        df = pd.DataFrame(mp_comps)

        companies_new = []

        for i in mp_comps:
            company = 'Неопределена'
            dist0 = 0

            for val in spie_comps:
                dist = fuzz.token_sort_ratio(i, val)
                if dist > dist0:
                    dist0, company = dist, val
            companies_new.append(company)

        self.df_result['Spie_company'] = companies_new


class UrlGrouping:
    def __init__(self, df):
        self.df = df

    def url_group(self):
        df1 = self.df.groupby('Url1').agg({'Wavelength_p': 'mean', 'Energy_p': 'mean', 'Wavelength_f': 'mean',
                                      'Energy_f': 'mean', 'Wavelength': 'mean', 'Energy': 'mean', 'Price': 'mean',
                                      'Shipment': 'mean', 'Total_x': 'sum', 'Total_y': 'sum', 'Total_medicine': 'sum'})

        df2 = self.df.groupby("Url1")[["Company"]].agg(lambda column: "    ".join(column))
        df1['Company'] = df2['Company'].str.split('    ').str[0]
        df1 = df1.reset_index()

        return df1


if __name__ == '__main__':
    # Merging data
    grouped_obj = GroupMaking()
    merged_df = grouped_obj.merge_products()

    # Adding URLs from Google
    urls_obj = UrlQuery(merged_df)
    urls_df = urls_obj.create_urls()

    # Grouping companies by URLs
    comps_grouped = UrlGrouping(urls_df)
    comps_df = comps_grouped.url_group()

    # Adding URL's statistcs
    webstat_obj = WebStatQuery(comps_df)
    webstat_obj.aws_query()
    df_result = webstat_obj.data

    # df_result.to_excel(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\merged_companies.xlsx')
