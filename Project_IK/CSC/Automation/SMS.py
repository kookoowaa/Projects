import os
import pandas as pd
import pyodbc
import datetime


days = input('How many days in advance do you require the data to be ready for SMS? ' )

query = '''
select  
    a.AssignAgent,
    convert(varchar(10), a.insertDate,112) + replace(convert(varchar(8),a.insertdate,108),':','') as TimeOfCS,
    a.CallID,
    a.AssignAgent,
    a.TelNumber,
    SUBSTRING(b.wrapupCode, 1, 2) as WrapupCode
    --b.WorkgroupID,
    --row_number() over (partition by SUBSTRING(wrapupCode, 1, 2) order by SUBSTRING(wrapupCode, 1, 2)) as 'row_number'
from
    I3_IC.dbo.T_SMS_Info as a,
    I3_IC.dbo.InteractionWrapup b
where
    a.CallID = b.interactionIDKey
    and TelNumber like '010%'
    and CusomSting1 = 'Y'
    and assignagent not like 'T[0-9]' 
    and wrapupCode <> 'NS'
    and a.InsertDate >= cast(getdate()-{d} as date)
    and a.InsertDate < cast(getdate() as date)
    --and substring(calleventlog, charindex('Press Log : 0', calleventlog)+25, 13) != 'Press Log : 1'
    -- 상담원 연결(Press Log:0) 이후 문자수신 거부한(press log:1) 고객은 대상에서 제외
'''.format(d= days)

print('accessing db...')

try:
    conn = pyodbc.connect(server = 'RETKRCSC-NT8004', database = 'I3_IC', Trusted_Connection='yes', driver = '{ODBC Driver 13 for SQL Server}')
except:
    print('connection error')

df = pd.read_sql(query, conn)

"""
idx = [i%2==0 for i in df.index]
df = df[idx]
"""
rounds = int(len(df)/100)+1


for i in range(rounds):
    tmp = df[0+i*100:99+i*100]
    tmp.to_excel(r'C:\Users\chpar10\IKEA\CSC individual contributors (RETKRCSC) - 문서\KMI\NPS\SMS\SMS({d}){n}.xlsx'
                 .format(d=datetime.datetime.now().strftime('%m%d'),n=i), index=False)

print('process finished with {n}-files'.format(n=rounds))
os.startfile(r'C:\Users\chpar10\IKEA\CSC individual contributors (RETKRCSC) - 문서\KMI\NPS\SMS')


