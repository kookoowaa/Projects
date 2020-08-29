#///////////////////////////////////////////////////////////////////////////////////
# File Name......: crawler.py
# Auther.........: Pablo Park
# Written date...: 28 Aug. 2020
# Last updated...: 28 Aug. 2020
# Description....: Crawling store opening status
# Dependancies...: python 3.8.3
#                  requests 2.24.0
#                  beautifulsoup4 4.9.1
#///////////////////////////////////////////////////////////////////////////////////

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

tmp = pd.read_excel('sto_list.xlsx')
tmp = tmp[~tmp['Site address'].isna()]
tmp = tmp.reset_index(drop=True)

outcome = []
for add in tmp['Site address']:
    html_get = requests.get(add)
    html = bs(html_get.text, 'html.parser')
    try:
        opening = html.find_all(attrs={'name':'opening-hours'})[0].text
        if opening[-6:] == 'Closed':
            outcome.append('Closed')
        else:
            outcome.append('Open')
    except IndexError:
        outcome.append('Invalid address')

fout = pd.concat([tmp,pd.DataFrame(outcome, columns = ['Open'])], axis=1)
fout.to_excel('Store status.xlsx', index=False)