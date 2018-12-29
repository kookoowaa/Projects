# Author.............: Park, Pablo Chanwoo
# File name..........: weekly.py
# Written Date.......: 2018-12-28
# Program Description: program automation for crawling and processing weekly report data for Malaysia

from selenium import webdriver
import pandas as pd
import numpy as np
import re
import time
import datetime
import os


## Define variables
#### Define chromedriver
driver = webdriver.Chrome("d:/git/chromedriver.exe")

#### Define stores to crawl data from
stores = ["arcoris", "ipc", "setia-city", "mytown", "genting", "pearl", "penang", "sunway-pyramid", "pavilion", "1-utama"]

#### Define date variables
date_from= []
date_from.append(input('date from(dd): '))
date_from.append(input('month from(mm): '))
date_from.append(input('year from(yyyy): '))
range_from = date_from[0]+'%2F'+date_from[1]+'%2F'+date_from[2]+'+00%3A00%3A27'

date_to= []
date_to.append(input('date to(dd): '))
date_to.append(input('month to(mm): '))
date_to.append(input('year to(yyyy): '))
range_to = date_to[0]+'%2F'+date_to[1]+'%2F'+date_to[2]+'+00%3A00%3A27'

#### Define html links to crawl data from
sales_summary = 'https://kyochon.revelup.com/brand/reports/sales_summary/json/?dining_option=&employee=&online_app=&online_app_type=&online_app_platform=&show_unpaid=1&show_irregular=1&range_from={}&range_to={}&format=csv'.format(range_from, range_to)
hourly_sales = 'https://kyochon.revelup.com/reports/hourly_sales/export/csv/?aggregate_format=hours&employee=&online_app=&online_app_type=&online_app_platform=&dining_option=&show_unpaid=1&show_irregular=1&no-filter=0&day_of_week=&range_from={}&range_to={}'.format(range_from, range_to)
product_mix = 'https://kyochon.revelup.com/reports/product_mix/data/?sort_by=&sort_reverse=&combo_expand=&employee=&online_app=&online_app_type=&online_app_platform=&dining_option=&show_unpaid=1&show_irregular=1&sort_view=1&show_class=1&quantity_settings=0&no-filter=0&day_of_week=&range_from={}&range_to={}&format=csv'.format(range_from, range_to)
#### NOTE that the report can be downloaded via URL API, per store you are logged onto (28 Dec. 2018)

#### Define directory
user_name = input("Enter your user name please (to access download folder): ")
directory = 'D:/Users/{}/Downloads/'.format(user_name)  ## adjustment maybe needed accordingly
print("Initiating program...")
beginning = time.time()



## Define functions
#### function to sort sales by menu
def pd_mix_func(file):
    global tmp_pd, sales_by_menu
    
    try:
        tmp_pd = pd.merge(pd.read_csv(directory+file, engine='python').groupby("Class", as_index=False).sum(),
                   menu,
                   left_on="Class",
                   right_on = "asis").groupby('tobe').sum()['Total Sales']
    except:
        for i in range(len(tmp_pd)):
            tmp_pd[i] = np.NaN
    if store == stores[0]:
        sales_by_menu = pd.DataFrame(tmp_pd)
    else:
        sales_by_menu = pd.concat([sales_by_menu, pd.DataFrame(tmp_pd)], axis = 1, sort = False)
    sales_by_menu = sales_by_menu.drop("Delete")
    
#### function to sort sales by time
def hourly_func(file):
    global sales_by_time
    
    temp = pd.read_csv(directory+file, engine='python')[['Time', 'Sales']].iloc[9:24]
    
    if store == stores[0]:
        sales_by_time = pd.DataFrame(temp)
    else:
        sales_by_time = pd.concat([sales_by_time, pd.DataFrame(temp)["Sales"]], axis = 1, sort = False)

#### function to sort sales by day, and sales by order type
def sales_func(file):
    global daily_gross_sales, daily_net_sales, sales_by_order
    
    
    temp = pd.read_csv(directory+file, engine='python')#[['Gross Sales', 'Net Sales','Togo Sales', 'Eatin Sales', 'Delivery Sales',
                                                       # 'Catering Sales', 'WebOrder', 'Online Sales', 'Shipping Sales', 'Takeaway']]
    temp1 = pd.DataFrame([temp[['Eatin Sales', 'Catering Sales']].sum().sum(),
                         temp[['Togo Sales', 'Takeaway']].sum().sum() ,
                         temp[['Delivery Sales', 'Online Sales', 'Shipping Sales']].sum().sum()],
                        index = ['Dining', 'Take-out', 'Delivery'])
    
    if store == stores[0]:
        daily_gross_sales = pd.DataFrame(temp['Gross Sales'])
        daily_net_sales = pd.DataFrame(temp['Net Sales'])
        sales_by_order = temp1
    else:
        daily_gross_sales = pd.concat([daily_gross_sales,temp['Gross Sales']], axis = 1, sort = False)
        daily_net_sales = pd.concat([daily_net_sales,temp['Net Sales']], axis = 1, sort = False)
        sales_by_order = pd.concat([sales_by_order, temp1], axis = 1, sort = False)
        


## Access web-site //line 14: driver = webdriver.Chrome("d:/git/chromedriver.exe")//
#### Open the web-site
driver.get("https://kyochon.revelup.com/login/?next=/dashboard/") # POS web-site
driver.implicitly_wait(3)

#### Log-in
driver.find_element_by_xpath('//*[@id="id_username"]').send_keys("JayceKim")
driver.find_element_by_xpath('//*[@id="id_password"]').send_keys("Qwer1234!!")
driver.find_element_by_xpath('//*[@id="form-login"]/fieldset/div[3]/input').click()
driver.implicitly_wait(3)

#### Open store lists
driver.find_element_by_xpath('//*[@id="header"]/div[2]/div[2]/div[2]').click()
time.sleep(5)

#### Retrieve total number of stores
tmp = driver.find_element_by_class_name('fancytree-title').text
n_store = int(re.findall(string=tmp, pattern = '[0-9]+')[0])

#### Fetch data from the web-site 
for i in range(1, n_store+1):
    print('data fetching on store #{}...'.format(str(i)))
    #### Access Store
    if i > 1:
        driver.find_element_by_xpath('//*[@id="header"]/div[2]/div[2]/div[2]').click()
        time.sleep(5)
    driver.find_element_by_xpath('//*[@id="establishments-tree"]/div/div[3]/ul/li[1]/ul/li[{}]/span[2]/span[3]'.format(i)).click()
    time.sleep(5)
    
    #### Run URL APIs
    driver.get(sales_summary)
    driver.implicitly_wait(3)
    driver.get(hourly_sales)
    driver.implicitly_wait(3)
    driver.get(product_mix)
    driver.implicitly_wait(3)



## Sort menus
#### Read fetched data
for i in stores:
	#### Read files
    product_mix = "Product_Mix_{}_{}_00-00_{}_00-00.csv".format(i,
                                                            (date_from[2] + '-' +date_from[1] +'-'+ date_from[0]),
                                                            (date_to[2] + '-' +date_to[1] +'-'+ date_to[0]))
    #### Group by classes
    if i =='arcoris':
        tmp = pd.read_csv(directory+product_mix).groupby('Class', as_index = False).sum()
    else:
    	#### In case file is empty, pass the file
        try:
            tmp = pd.concat([tmp, pd.read_csv(directory+product_mix).groupby('Class', as_index = False).sum()])
        except:
            pass

#### Retrieve unique menus
tmp = tmp.Class.unique()
tmp.sort()

#### Re-group categories for report ("Beverage", "Chicken", "Side", "Salad", "A-La-Carte")
#### If previous classification is avaiable, read
if pd.Series(os.listdir('weekly/')).isin(["menu.csv"]).sum() == 1:
	menu = pd.read_csv('weekly/menu.csv')
#### If not, make classification.
#### The below "tobe" may need rearrangement
else:
	tobe = ["A-La-Carte", "Beverage", "Beverage", "Beverage", "Chicken",
			"Delete", "Delete", "Chicken", "Beverage", "Chicken",
 			"Beverage", "Chicken", "Beverage", "Side", "Chicken", 
 			"Chicken", "Salad", "Delete", "Side", "Beverge"]
	menu = pd.DataFrame([tmp, tobe]).T
	menu.columns = ['asis', 'tobe']
	#### final menu to be saved as csv
	menu.to_csv("weekly/menu.csv")



## Read process data per report
for store in stores:
	#### call reports per store and run user-defined-function
    product_mix = "Product_Mix_{}_{}_00-00_{}_00-00.csv".format(store,
                                                            (date_from[2] + '-' +date_from[1] +'-'+ date_from[0]),
                                                            (date_to[2] + '-' +date_to[1] +'-'+ date_to[0]))
    hourly_sales = "Hourly_Sales_{}_{}_00-00_{}_00-00.csv".format(store,
                                                            (date_from[2] + '-' +date_from[1] +'-'+ date_from[0]),
                                                            (date_to[2] + '-' +date_to[1] +'-'+ date_to[0]))
    sales_summary = "Sales_Summary_{}_{}_00-00_{}_00-00.csv".format(store,
                                                            (date_from[2] + '-' +date_from[1] +'-'+ date_from[0]),
                                                            (date_to[2] + '-' +date_to[1] +'-'+ date_to[0]))
    pd_mix_func(product_mix)
    hourly_func(hourly_sales)
    sales_func(sales_summary)
    
    #### at last store, assign column names to each report DataFrame
    if store == stores[-1]:
        sales_by_time.columns = ['Time'] + stores
        sales_by_menu.columns = stores
        daily_gross_sales.columns = stores
        daily_net_sales.columns = stores
        sales_by_order.columns = stores



## Merge reports onto one excel sheet
writer = pd.ExcelWriter('Weekly/weekly_report({}{}-{}{}).xlsx'.format(date_from[1], date_from[0], date_to[1], date_to[0]), engine='xlsxwriter')

daily_net_sales.to_excel(writer, sheet_name="raw data")
daily_gross_sales.to_excel(writer, sheet_name="raw data", startrow=9)
sales_by_order.to_excel(writer, sheet_name="raw data", startrow=9+9)
sales_by_menu.to_excel(writer, sheet_name="raw data", startrow=9+9+5)
sales_by_time.to_excel(writer, sheet_name="raw data", startrow=9+9+5+9, index=False)

writer.save()

elap_min, elap_sec = np.divmod(time.time()-beginning, 60)
print("Total process finished at {}min, {}second". format(int(elap_min), int(elap_sec)))