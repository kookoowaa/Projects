#!/usr/bin/env python
# coding: utf-8

# In[12]:


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import openpyxl


# In[5]:


def parse_date(txt):
    date_begin = re.compile('categories: \[')
    date_begin = date_begin.search(txt).span()[1]
    date_end = re.compile('\]},yAxis:')
    date_end = date_end.search(txt).span()[0]
    
    return txt[date_begin:date_end].replace('"','').split(',')
    
    
def parse_data(txt):
    data_begin = re.compile('data: \[')
    data_begin = data_begin.search(txt).span()[1]
    data_end = re.compile('\]}\],responsive')
    data_end = data_end.search(txt).span()[0]
    tmp = txt[data_begin:data_end].split(',')
    tmp = [int(i) for i in tmp]
    
    return tmp


# In[6]:


def txt_to_html(txt):
    case_compile = re.compile('Total Coronavirus Cases')
    death_compile = re.compile('Total Coronavirus Deaths')
    
    for script in txt.find_all(attrs={'type':"text/javascript"}):
        try:
            if bool(case_compile.search(script.contents[0])):
                total_case = script.contents[0]
            elif bool(death_compile.search(script.contents[0])):
                total_death = script.contents[0]
        except:
            pass
        
#    total_case = txt.find_all(attrs={'type':"text/javascript"})[6].contents[0]
    total_case  = total_case.replace('\n','').replace('\'', '"').replace('    ','')
 #   total_death = txt.find_all(attrs={'type':"text/javascript"})[8].contents[0]
    total_death  = total_death.replace('\n','').replace('\'', '"').replace('    ','')
    
    case_date = parse_date(total_case)
    case_data = parse_data(total_case)
    death_date = parse_date(total_death)
    death_data = parse_data(total_death)
   
    return {"case_date":case_date, 'case_data':case_data,
            'death_date': death_date, 'death_data':death_data}


# In[7]:


def crawl_country(cnts):
    address = 'https://www.worldometers.info/coronavirus/country/'
    outcome = {}
    
    for cnt in cnts:
        web_add = address+'{}'.format(cnt)
        html = requests.get(web_add)
        soup = bs(html.text, 'html.parser')
        html.close()
        tmp = txt_to_html(soup)   
        outcome[cnt] = tmp
    
    return outcome


# In[8]:


cnt_list = ['UK', 'France', 'Germany', 'Spain', 'Australia']


# In[9]:


outcome = crawl_country(cnt_list)


# In[35]:


fout = 'COVID_worldometer.xlsx'


# In[36]:


wb = openpyxl.Workbook()
wb.save(fout)


# In[44]:


with pd.ExcelWriter(fout) as ew:
    for cnt in cnt_list:
        df = pd.DataFrame(outcome[cnt]).iloc[:,[0,1,3]][::-1]
        df.to_excel(ew, sheet_name=cnt, index=False)

