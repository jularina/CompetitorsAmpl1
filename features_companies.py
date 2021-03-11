import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

diodes_companies = pd.read_csv(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_diodes.csv', index_col='Unnamed: 0')
pics_companies = pd.read_csv(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_picosecond.csv', index_col='Unnamed: 0')
fems_companies = pd.read_csv(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_femtosecond.csv', index_col='Unnamed: 0')
spie_companies = pd.read_csv(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\parsed_companies.csv', index_col='Unnamed: 0')

diodes_companies = diodes_companies.drop_duplicates()[['Company', 'Wavelength','Energy','Price']]
pics_companies = pics_companies.drop_duplicates()[['Company', 'Wavelength','Energy']]
fems_companies = fems_companies.drop_duplicates()[['Company', 'Wavelength','Energy']]
diodes_companies['Price'] = diodes_companies['Price'].str.slice(start=1).str.replace(',','')
diodes_companies['Price'] = diodes_companies['Price'].astype(float)

cols = ['Wavelength', 'Energy']
dfs = [diodes_companies, pics_companies, fems_companies]
for df in dfs:
    df.replace({'  —': np.NaN}, inplace=True)
    for col in cols:
        df[col] = df[col].str.split().str[0]
        df[col] = df[col].astype(float)
    df.fillna(value=df.quantile(q=0.25), inplace=True)

pics_companies.rename(columns={'Wavelength':'Wavelength_p','Energy':'Energy_p'}, inplace=True)
fems_companies.rename(columns={'Wavelength':'Wavelength_f','Energy':'Energy_f'}, inplace=True)
pics_companies = pics_companies.groupby(by=["Company"]).median().reset_index()
fems_companies = fems_companies.groupby(by=["Company"]).median().reset_index()
diodes_companies = diodes_companies.groupby(by=["Company"]).median().reset_index()

df_result = pics_companies.merge(fems_companies, left_on='Company', right_on='Company', how='outer')
df_result = df_result.merge(diodes_companies, left_on='Company', right_on='Company', how='outer')
df_result['Price'].fillna(df_result['Price'].mean(), inplace=True)
df_result.fillna(0, inplace=True)

mp_comps = list(df_result['Company'])
spie_comps = list(set(spie_companies['Company']))
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

df_result['Spie_company'] = companies_new
df_result.to_excel(r'C:\Users\maxim\OneDrive\Desktop\folder\diplom\data\parsing\merged_companies.xlsx')

