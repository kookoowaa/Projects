import requests
import json
import pandas as pd
from datetime import date
from datetime import timedelta
import time
import ctypes


weekago = date.today() - timedelta(days=7)
weekago = weekago.isoformat()
dateofsurvey = input('yyyy-mm-dd: ')
print('crawling data from {}\n'.format(dateofsurvey))
try:
    dateofsurvey
except NameError:
    dateofsurvey = weekago
page = 1
per_page = 20
api_token = '?api_token=794270175edb08aba92eb522becb9f8fedb1f558f71589ee94'
api_secret = '&api_token_secret=A9NgssS5EgNPY'
fromwhen = '&filter[field][0]=date_submitted&filter[operator][0]=>&filter[value][0]={t}'.format(
    t=dateofsurvey)
perpage = '&page={p}&resultsperpage={pp}'.format(p=page, pp=per_page)
complete = '&filter[field][1]=status&filter[operator][1]=!=&filter[value][1]=Disqualified'

print('retrieving relevant information....\n')
tmp = requests.get('https://restapi.surveygizmo.eu/v5/survey/90206632/surveyresponse{apit}{apis}{survdate}{perpage}{comp}'.format(
    apit=api_token, apis=api_secret, survdate=fromwhen, perpage=perpage, comp=complete))
json_file = json.loads(tmp.text)
nLoop = json_file['total_pages']


tmp_dict = {'id': [], 'date': [], 'touchpoint': [], 'interaction_id': [
], 'CSAT': [], 'resolution': [], 'first_contact': [], 'freetext': []}
print('initiating....')
for cnt in range(nLoop):
    perpage = '&page={p}&resultsperpage={pp}'.format(p=page, pp=per_page)
    tmp = requests.get('https://restapi.surveygizmo.eu/v5/survey/90206632/surveyresponse{apit}{apis}{survdate}{perpage}{comp}'.format(
        apit=api_token, apis=api_secret, survdate=fromwhen, perpage=perpage, comp=complete))
    json_file = json.loads(tmp.text)

    for survey in json_file['data']:
        tmp_dict['id'].append(survey['id'])
        tmp_dict['date'].append(survey['date_submitted'][:10])
        try:
            tmp_dict['touchpoint'].append(
                survey['survey_data']['227']['answer'])
        except:
            tmp_dict['touchpoint'].append(None)
        try:
            tmp_dict['interaction_id'].append(
                survey['survey_data']['221']['answer'])
        except KeyError:
            tmp_dict['interaction_id'].append(None)
        try:
            for i in survey['survey_data']['77']['options']:
                tmp_dict['CSAT'].append(
                    survey['survey_data']['77']['options'][i]['answer'])
        except KeyError:
            tmp_dict['CSAT'].append(None)
        try:
            tmp_dict['resolution'].append(
                survey['survey_data']['250']['answer'])
        except KeyError:
            tmp_dict['resolution'].append(None)
        try:
            tmp_dict['first_contact'].append(
                survey['survey_data']['251']['answer'])
        except KeyError:
            tmp_dict['first_contact'].append(None)
        try:
            tmp_dict['freetext'].append(survey['survey_data']['231']['answer'])
        except KeyError:
            tmp_dict['freetext'].append(None)
    print('round {}/{}, complete'.format(page, nLoop))

    page += 1
print()
page = 1


print('generating reports...')
time.sleep(3)
tmp_df = pd.DataFrame(tmp_dict)


def validateSurvey(x):
    if x[4] == None:
        if x[5] == None:
            if x[6] == None:
                if x[7] == None:
                    return 0
    else:
        return 1


final_df = tmp_df[tmp_df.apply(validateSurvey, axis=1) == 1]


final_df.to_csv('c:/users/chpar10/OneDrive - IKEA/DA/PulseCX({f}-{t}).csv'.format(
    f=dateofsurvey, t=date.today().isoformat()), encoding='utf-8-sig', index=False)
ctypes.windll.user32.MessageBoxW(0, "process finished", "PulseCX Crawling", 0)
os.startfile('C:/Users/chpar10/OneDrive - IKEA/DA')
