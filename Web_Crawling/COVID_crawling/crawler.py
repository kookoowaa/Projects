# author: Pablo Park
# source: https://github.com/kookoowaa/Projects/blob/master/crawler.py
# last update: 2021 January 25th //날짜 데이터 포맷 변경

# Required libraries
import requests                           # requests: url 주소를 토대로 서버에서 html 데이터 수집을 가능케 함
from bs4 import BeautifulSoup as bs       # bs4: requests로 가져온 html 데이터를 navigate
import pandas as pd                       # pandas: 데이터 조작
import re                                 # re: 텍스트 검색
import openpyxl                           # openpyxl: 엑셀 파일 생성 및 저장


# html에서 날짜만 가져오는 함수
# html에서 날짜는 문자데이터로, "categories: [날짜1, 날짜2, 날짜3...]},yAxis:..." 구조로 구성
# date_begin에 첫번째 날짜 시작 인덱스를 date_end에 마지막 날짜 인덱스를 저장한 후, csv로 구성된 날짜 데이터를 리스트로 반환

def parse_date(txt):
    date_begin = re.compile('categories: \[')
    date_begin = date_begin.search(txt).span()[1]
    date_end = re.compile('\]},yAxis:')
    date_end = date_end.search(txt).span()[0]
    
    tmp = txt[date_begin:date_end].split('","')
    tmp = [i.replace('"','') for i in tmp]
    return tmp ## 날짜 데이터에 연도 데이터가 추가되면서 replace 함수 제거
    

# html에서 데이터를 가져오는 함수
# 날짜를 가져오는 함수와 동일한 로직을 사용하고, 다만 구조는 "data: [데이터1, 데이터2, 데이터3]}],responsive..."형태임
def parse_data(txt):
    data_begin = re.compile('data: \[')
    data_begin = data_begin.search(txt).span()[1]
    data_end = re.compile('\]}\],responsive')
    data_end = data_end.search(txt).span()[0]
    tmp = txt[data_begin:data_end].split(',')
    tmp = [int(i) for i in tmp]
    
    return tmp


# 수집한 html에서 데이터를 추출하는 함수
# 인풋은 html이, 아웃풋은 Python dictionary(JSON)이 됨
# 함수 로직은 전체 html에서 1) "text/javascript"에 해당하는 html만 분리하고,
#                         2) 분리한 "text/javascript"에서 "Total Coronavirus Cases"와 "Total Coronavirus Deaths"가 포함되어 있는 html만 남겨둠
# 이후 위에서 만들어둔 parse_date()와 parse_data()를 사용하여 html에서 데이터만 분리
# 분리한 데이터를 dictionary 형태로 정제하여 아웃풋으로 제공
def html_manipulation(html):
    case_compile = re.compile('Total Coronavirus Cases')
    death_compile = re.compile('Total Coronavirus Deaths')
    
    for script in html.find_all(attrs={'type':"text/javascript"}):
        try:
            if bool(case_compile.search(script.contents[0])):
                total_case = script.contents[0]
            elif bool(death_compile.search(script.contents[0])):
                total_death = script.contents[0]
        except:
            pass
        
#   total_case = html.find_all(attrs={'type':"text/javascript"})[6].contents[0]
    total_case  = total_case.replace('\n','').replace('\'', '"').replace('    ','')
#   total_death = html.find_all(attrs={'type':"text/javascript"})[8].contents[0]
    total_death  = total_death.replace('\n','').replace('\'', '"').replace('    ','')
    
    # 사전 정의된 사용자 함수 사용
    case_date = parse_date(total_case)
    case_data = parse_data(total_case)
    death_date = parse_date(total_death)
    death_data = parse_data(total_death)
   
    return {"case_date":case_date, 'case_data':case_data,
            'death_date': death_date, 'death_data':death_data}


# html을 수집하는 함수
# 인풋은 국가명으로 이루어진 리스트이며, 아웃풋은 html_manipulation에서 만든 dictionary가 국가 단위로 계층화 된 dictionary(json)임
# (계층형 데이터: 국가 > date/nCase/nDeath > 데이터)
# 리스트를 인풋으로 받으면 리스트의 순서대로 iterate 하면서 데이터를 수집하고, 위에서 정의한 html_manipulation() 함수를 호출하여 데이터만 정제
def crawl_country(cnts):
    address = 'https://www.worldometers.info/coronavirus/country/'
    outcome = {}
    
    for cnt in cnts:
        web_add = address+'{}'.format(cnt)
        html = requests.get(web_add)
        soup = bs(html.text, 'html.parser')
        html.close()
        tmp = html_manipulation(soup)   
        outcome[cnt] = tmp
    
    return outcome


####################
### 함수정의 완료 ### 
### 프로그램 실행 ###
####################


# 추출 대상 국가 정의 ('https://www.worldometers.info/coronavirus/country/{국가명}')
cnt_list = ['UK', 'France', 'Germany', 'Spain', 'Australia']

# 위에서 정의내린 최상위 사용자 함수 실행하여 outcome 변수에 결과 값 할당
outcome = crawl_country(cnt_list)


#############################
### 데이터추출 및 정제 완료 ###
### 엑셀로 데이터 변환      ###
#############################


# 출력 파일명 및 위치 정의
fout = 'COVID_worldometer.xlsx'

# 엑셀 파일 생성
wb = openpyxl.Workbook()
wb.save(fout)

# pandas로 엑셀파일을 열고, 위에서 정의 내린 국가명 cnt_list에 따라 시트를 생성하고 표 형식으로 데이터 저장
with pd.ExcelWriter(fout) as ew:
    for cnt in cnt_list:
        df = pd.DataFrame(outcome[cnt]).iloc[:,[0,1,3]][::-1]
        df.to_excel(ew, sheet_name=cnt, index=False)


####################
### 프로그램 종료 ###
####################
