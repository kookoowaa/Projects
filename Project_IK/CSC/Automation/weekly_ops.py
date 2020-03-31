#!/usr/bin/env python
# coding: utf-8


import os
import pandas as pd
import pyodbc
import datetime
import time


week_number = input('week: data for week... ')


conn = pyodbc.connect(server = 'RETKRCSC-NT8004', database = 'I3_IC', Trusted_Connection='yes', driver = '{ODBC Driver 13 for SQL Server}')


# 2월 명단 반영 (2/17)
frontline = """
'HYLEE13', 'SEMOO3', 'SOPZR3', 'KYKAN', 'WOKAN1',
'SUKIM21', 'WOSEO', 'SEYUN', 'MOLEE3', 'YOLEE32',
'SELEE42', 'DOKIM27', 'EUSON', 'YOPAR3', 'SULEE37',
'EUKWO', 'OCKIM', 'SEYOH2', 'SOYOU3', 'MILIM3',
'BYKIM7', 'MYLEE6', 'YOKIM17', 'HYGOO', 'YUKOH1',
'EULIM3', 'JAHON1', 'HYCHO20', 'SUKIM16', 'YOJEO3',
'DALEE2', 'AYHON', 'SUSON1', 'KYLEE11', 'KYLEE21',
'JAKIM20', 'SEKIM30', 'MINJO2', 'NAKIM11', 'MIJUN2',
'JUYOO1',


'EUKAN10', 'yejun1',
'YELEE18', 'HEHAN4', 'YOSEO5', 'HACHO9', 'hylee46'
"""
##두번째 문단은 UBASE 인원
email ="""
'SELEE19', 'SULEE19', 'HOPAR4', 'HYLEE40'
"""

data_format = [
[],
 ['transaction', 'call(inbound)', 'chat(inbound)', 'call(offered)',
  'chat(offered)', 'email(offered)', 'call(answered)', 'chat(answered)', 'email(answered)', 
  'svl_call(30s)', 'svl_call(60s)', 'svl_chat', 'svl_email', 'call_answered(30s)_YTD', 
  'call_answered(60s)_YTD', 'call_offered_YTD', 'chat_answered(30s)_YTD', 'chat_offered_YTD', 'email_answered(1d)_YTD',
  'email_offered_YTD', 'svl_call(FY20)'  ,
  'svl_chat(FY20)', 'svl_email(FY20)', 'aht_call', 'aht_chat', 'aht_email', 
  'cph_call', 'cph_chat', 'utilization', 'time_상담가능', 'time_상담중', 
  'time_후처리', 'call_by_fl', 'call_by_email', 'call_by_else', 'chat_by_email', 
  'chat_by_fl', 'nvac_share', 'nvac/1000', 'sales_csc', 'sales_kitchen', 'sales_to_ecom'],
[]]



weekly_index = pd.DataFrame(data_format, index = ['주차', '데이터 구분', '값']).T
weekly_index.주차 = week_number


# ## Queries

# ### 1. Query for Inbound and Correlation

query = '''
select
    count(CallEventLog)
from
    I3_IC.dbo.calldetail_viw
Where
	InitiatedDate >= getdate() - 31
	and Datepart(week, InitiatedDate) = {w}
	and [CallType] = 'external'
	and [AssignedWorkGroup] != '%outbound%'
	and [CallDirection] != 'Outbound'
	and lineid = 'UDP5060'
group by
	dATEPART(week, InitiatedDate)
'''.format(w=week_number)


tmp = pd.read_sql(query, conn)

weekly_index.loc[weekly_index['데이터 구분']=='call(inbound)', '값'] = int(tmp.iloc[0])

print('1/5 finished')

# ### 2. Query for Offered, Answered, SVL


query = '''
SELECT
	datepart(week, dintervalstart) as 'week',
	chkey3 as 'type',
	sum(nenteredacd) as 'offered',
	sum(nansweredacd) as 'answered',
    /*
	cast(
        ISNULL((sum(([tAnsweredAcd])*1.0)/nullif(sum([nenteredacd]),0)*1.0), 0)
        as decimal(10,2)
        ) As 'ASA',
    */
	cast(
        sum(nAnsweredAcdSvcLvl1) * 1.0/nullif(sum(nenteredacd),0)
        as decimal(10,4)
        ) As 'Call SL 30',
	cast(
        (sum([nAnsweredAcdSvcLvl1]) + sum([nAnsweredAcdSvcLvl2]) + sum([nAnsweredAcdSvcLvl3]) + sum([nAnsweredAcdSvcLvl4])) * 1.0/nullif(sum([nenteredacd]), 0)
        as decimal(10,4)
        ) As 'Call SL 60',
	cast(
        (sum([nAnsweredAcdSvcLvl1]) + sum([nAnsweredAcdSvcLvl2])) * 1.0/nullif(sum([nansweredacd]),0)
        as decimal(10,4)
        ) As 'Email SL'
FROM
    I3_IC.dbo.IWrkgrpQueueStats
WHERE
    dIntervalStart > getdate()-31
	and datepart(week, dintervalstart) = {w}
	and (cHKey4 != '*' AND cReportGroup != '*')
    and (cName like '%KR%')
GROUP BY
	datepart(week, dintervalstart),
	CHKey3
'''.format(w=week_number)


tmp = pd.read_sql(query, conn)
tmp = tmp.set_index('type')


weekly_index.loc[weekly_index['데이터 구분']=='call(offered)', '값'] = int(tmp.loc['Call','offered'])
weekly_index.loc[weekly_index['데이터 구분']=='email(offered)', '값'] = int(tmp.loc['Email Interaction', 'offered'])
weekly_index.loc[weekly_index['데이터 구분']=='call(answered)', '값'] = int(tmp.loc['Call', 'answered'])
weekly_index.loc[weekly_index['데이터 구분']=='email(answered)', '값'] = int(tmp.loc['Email Interaction', 'answered'])

weekly_index.loc[weekly_index['데이터 구분']=='svl_call(30s)', '값'] = float(tmp.loc['Call', 'Call SL 30'])
weekly_index.loc[weekly_index['데이터 구분']=='svl_call(60s)', '값'] = float(tmp.loc['Call', 'Call SL 60'])
weekly_index.loc[weekly_index['데이터 구분']=='svl_email', '값'] = float(tmp.loc['Email Interaction', 'Email SL'])

print('2/5 finished')

# ### 3. Query for SVL YTD


query = '''
SELECT
	chkey3 as 'type',
	sum(nenteredacd) as 'offered',
	sum(nAnsweredAcdSvcLvl1) as 'answered1',
    sum([nAnsweredAcdSvcLvl1]) + sum([nAnsweredAcdSvcLvl2]) + sum([nAnsweredAcdSvcLvl3]) + sum([nAnsweredAcdSvcLvl4]) as 'answered2',
    sum([nAnsweredAcdSvcLvl1]) + sum([nAnsweredAcdSvcLvl2]) as 'answered_email'
FROM
    I3_IC.dbo.IWrkgrpQueueStats
WHERE
    dIntervalStart > '2019-09-03' 
    and dIntervalStart < DATEADD(wk, DATEDIFF(wk, 6, getdate()), 6)
	and (cHKey4 != '*' AND cReportGroup != '*')
    and (cName like '%KR%')
GROUP BY
	CHKey3

'''

tmp = pd.read_sql(query, conn)


weekly_index.loc[weekly_index['데이터 구분']=='call_offered_YTD', '값'] = int(tmp.loc[0,'offered'])
weekly_index.loc[weekly_index['데이터 구분']=='call_answered(30s)_YTD', '값'] = int(tmp.loc[0, 'answered1'])
weekly_index.loc[weekly_index['데이터 구분']=='call_answered(60s)_YTD', '값'] = int(tmp.loc[0, 'answered2'])

weekly_index.loc[weekly_index['데이터 구분']=='email_offered_YTD', '값'] = int(tmp.loc[3, 'offered'])
weekly_index.loc[weekly_index['데이터 구분']=='email_answered(1d)_YTD', '값'] = int(tmp.loc[3, 'answered_email'])

weekly_index.loc[weekly_index['데이터 구분']=='svl_call(FY20)', '값'] = round(tmp.loc[0, 'answered1'] / tmp.loc[0, 'offered'], 4)
weekly_index.loc[weekly_index['데이터 구분']=='svl_email(FY20)', '값'] = round(tmp.loc[3, 'answered_email'] / tmp.loc[3,'offered'], 4)

print('3/5 finished')
# ### 4. FL performance

query = '''
SELECT
	t2.week,
	t1.total_call,
	t1.total_chat,
	t1.total_email,
	t2.[Hours(AHT)],	
	t2.[Hours(CPH)],
	t2.[상담가능],
	t2.[통화중],
	t2.[후처리],
	t2.Productivity,
	t2.Utilization as 'Utilization(%)',
	t2.[Hours(AHT)] / t1.total_call as 'AHT',
	cast(t1.total_call * 1.0 / t2.[Hours(CPH)] *3600 as decimal(10,2)) as 'CPH'


FROM
	(Select
			datepart(week, dintervalstart) as 'week',
			sum(case when cHKey4 = 'Call' then answeredSLTarget end) as 'total_call',
			sum(case when cHKey4 = 'Chat' then answeredSLTarget end) as 'total_chat',
			sum(case when cHKey4 = 'Email interaction' then answeredSLTarget end) as 'total_email'

		from
			I3_IC.dbo.AgentServiceLevel_viw
    
		where
	
			dIntervalStart > getdate() - 31
			and datepart(week, dintervalstart) = {wk}
			AND (cHKey4 != '*')
			and  (cReportGroup like '%KR%')
			and cname in ({fl})
			
    
		group by
			dATEPART(week, dintervalstart)
		)t1
		

	right join(
		SELECT
			datepart(week, statusdatetime) as 'week',
			sum(case when statuskey = 'available' then stateduration end) as N'상담가능',
			sum(case when statuskey = 'answering call' then stateduration end) as N'통화중',
			sum(case when statuskey in ('acw_follow up', 'acw_otherworks', 'acw_taking over') then stateduration end) as N'후처리',
			sum(stateduration) - sum(case when statuskey in ('bl_trainer', 'training', 'meeting', 'lunch', 'break') then stateduration end) as 'Productivity',
			cast(
				sum(case when statuskey in ('answering call', 'acw_follow up', 'acw_otherworks', 'acw_taking over', 'sales', 'acw_overtime') then stateduration end) *1.0/
				nullif(sum(case when statuskey in ('available', 'not answered', 'answering call', 'acw_follow up', 'acw_otherworks', 'acw_taking over', 'sales', 'acw_overtime') then stateduration end),0)
				as decimal(10,4)
				) as 'Utilization',
			sum(case when statuskey in
				('answering call', 'acw_follow up', 'acw_otherworks', 'acw_taking over', 'acw_overtime', 'sales')
				then stateduration end) as 'Hours(AHT)',
			sum(stateduration) - sum(case when statuskey in ('bl_trainer', 'training', 'meeting', 'lunch', 'break', 'idletime', 'store support', 'gone home', 'invalid status', 'coaching', 'answering chat 1', 'answering chat 2', 'email', 'available_chat')
				then stateduration end) as 'Hours(CPH)'
			
		FROM
			I3_IC.dbo.AgentActivityLog

		WHERE
			StatusDateTime > getdate()-31
			and datepart(week, statusdatetime) = {wk}
			and userId in ({fl})

		GROUP BY
			datepart(week, statusdatetime)
		) t2

	on t1.week = t2.week
'''.format(fl = frontline, wk=week_number)

tmp = pd.read_sql(query, conn)
tmp




weekly_index.loc[weekly_index['데이터 구분']=='aht_call', '값'] = int(tmp.loc[0,'AHT'])
weekly_index.loc[weekly_index['데이터 구분']=='cph_call', '값'] = round(tmp.loc[0,'CPH'], 2)
weekly_index.loc[weekly_index['데이터 구분']=='utilization', '값'] = round(tmp.loc[0,'Utilization(%)'], 4)

weekly_index.loc[weekly_index['데이터 구분']=='time_상담가능', '값'] = int(tmp.loc[0,'상담가능'])
weekly_index.loc[weekly_index['데이터 구분']=='time_상담중', '값'] = int(tmp.loc[0,'통화중'])
weekly_index.loc[weekly_index['데이터 구분']=='time_후처리', '값'] = int(tmp.loc[0,'후처리'])

weekly_index.loc[weekly_index['데이터 구분']=='call_by_fl', '값'] = int(tmp.loc[0,'total_call'])

print('4/5 finished')
# ### 5. Email performance


query = '''

SELECT
	t2.week
	, t1.total_call
	, t1.total_email
	, Null as 'total_chat'
	, t2.[chat_hours(AHT)]	
	, t2.[chat_hours(CPH)]
	--, t2.[email_hours(AHT)]
	, t2.[email_hours(AHT)] / t1.total_email as 'email_AHT'


FROM
	(Select
			datepart(week, dintervalstart) as 'week',
			sum(case when cHKey4 = 'Call' then answeredSLTarget end) as 'total_call',
			sum(case when cHKey4 = 'Email Interaction' then answeredSLTarget end) as 'total_email'

		from
			I3_IC.dbo.AgentServiceLevel_viw
    
		where
			dIntervalStart > getdate() - 31
			and datepart(week, dintervalstart) = {wk}
			AND (cHKey4 != '*')
			and  (cReportGroup like '%KR%')
			and cname in ({email})
    
		group by
			dATEPART(week, dintervalstart)
		)t1
		

	right join(
		SELECT
			datepart(week, statusdatetime) as 'week',
			sum(case when statuskey in
				('acw_overtime', 'answering chat 1', 'answering chat 2', 'available_chat', 'acw_otherworks')
				then stateduration end) as 'chat_hours(AHT)',
			sum(stateduration) - sum(case when statuskey in ('bl_trainer', 'training', 'meeting', 'lunch', 'break',
															'idletime', 'store support', 'gone home', 'invalid status', 'coaching',
															'email', 'answering call', 'acw_otherworks')
			--'acw_otherworks' 포함 여부 확인 필요
				then stateduration end) as 'chat_hours(CPH)',
			sum(case when statuskey in
				('email')
				then stateduration end) as 'email_hours(AHT)'
			
		FROM
			I3_IC.dbo.AgentActivityLog

		WHERE
			StatusDateTime > getdate()-31
			and datepart(week, statusdatetime) = {wk}
			and userid in ({email})

		GROUP BY
			datepart(week, statusdatetime)
		) t2
	on t1.week = t2.week
'''.format(wk=week_number, email = email)



tmp = pd.read_sql(query, conn)




weekly_index.loc[weekly_index['데이터 구분']=='aht_email', '값'] = int(tmp.loc[0,'email_AHT'])

weekly_index.loc[weekly_index['데이터 구분']=='call_by_email', '값'] = int(tmp.loc[0,'total_call'])

weekly_index.loc[weekly_index['데이터 구분']=='call_by_else', '값'] = (int(weekly_index.loc[weekly_index['데이터 구분']=='call(answered)', '값'])
																	- int(weekly_index.loc[weekly_index['데이터 구분']=='call_by_fl', '값'])
																	- int(weekly_index.loc[weekly_index['데이터 구분']=='call_by_email', '값']))

weekly_index.loc[weekly_index['데이터 구분']=='aht_chat', '값'] = int(tmp.loc[0,'chat_hours(AHT)'])
weekly_index.loc[weekly_index['데이터 구분']=='cph_chat', '값'] = int(tmp.loc[0,'chat_hours(CPH)'])

print('5/5 finished')


weekly_index.to_csv('c:/users/chpar10/OneDrive - IKEA/DA/weekly_ops_data(wk{}).csv'.format(week_number), index=False, encoding='utf-8-sig')

print('process finished...')

time.sleep(5)

os.startfile(r'C:\Users\chpar10\OneDrive - IKEA\DA\weekly_ops_data(wk{}).csv'.format(week_number))
os.startfile(r'C:\Users\chpar10\IKEA\CSC individual contributors (RETKRCSC) - 문서\0. CSC REPORT\Report\Ops Performance\FY20\Weekly\ops_performance.xlsx')
