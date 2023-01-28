import logging 
import pandas as pd
import json
import sqlalchemy as db
from sqlalchemy import engine,create_engine

import pymysql
from sqlalchemy import MetaData,Table, Column, Integer, String,Float,DateTime
import warnings
import logging  
import yfinance as yf
import datetime as dt
import pandas as pd




def gettest(company_name,company_code,conn):

    try:
    
        start_date = '2023-01-21'
        end_date = '2023-01-31'
        
        #stock_data = yf.download(company_code, start_date, end_date)
        stock_data = yf.download(company_code)

        stock_data['Company_Name']=company_name
        stock_data['Company_Code']=company_code

        stock_data=stock_data.reset_index()
        stock_data.to_sql('stock_data',con=conn,index=False,if_exists='append')

        return company_name
    except Exception as e:
        return e


def outputcount(conn):
    output_query='''
    select  b.cmp_code as 'Company DB ID',a.company_name as 'Company Name',a.company_code as 'Company Code',count(a.company_code) as Records,b.company_sector as 'Company Sector',date(min(a.Date)) as 'First Record',date(max(a.Date)) as 'Last Updated Record',datediff(max(a.Date),min(a.Date)) as 'No of days' from stock_data a
    left join company_code b on a.Company_Code=b.company_code
    group by b.cmp_code,a.company_name,a.company_code,b.company_sector
    order by  b.cmp_code desc
    '''
    result=conn.execute(output_query)
    df=pd.DataFrame(result)

    return df

def sector_list_query(conn):
    try:    
        select_sector_query='''
        select sector from sector'''
        sector_df=conn.execute(select_sector_query).fetchall()
        sector_df=pd.DataFrame(sector_df)
        sector_df=sector_df['sector']
        return sector_df
    except Exception as e:
        return 'Exception occurred :',e


def execute_yf_code(conn):
    max_query='''
      select company_name,company_code,date(max(date)) max_date,date_add(date(max(date)),interval 1 day) start_date,date(now()) end_date  from stock_data where company_code in ('NATIONALUM.NS') group by company_name,company_code;
      '''

    exec_df=pd.DataFrame(conn.execute(max_query))
    exec_df.head()


    stock_data_temp1=pd.DataFrame()
    stock_data_temp2=pd.DataFrame()

    for i in range(len(exec_df)):

        stock_data_temp1=yf.download(exec_df.loc[i]['company_code'], exec_df.loc[i]['start_date'], exec_df.loc[i]['end_date'])

        stock_data_temp1['Company_Name']=exec_df.loc[i]['company_name']
        stock_data_temp1['Company_Code']=exec_df.loc[i]['company_code']
        stock_data_temp1=stock_data_temp1.reset_index()

        stock_data_temp2=pd.concat([stock_data_temp1,stock_data_temp2])

    
    stock_data_temp2.to_sql('stock_data',con=conn,index=False,if_exists='append')    
    a=list(stock_data_temp2['Company_Code'].unique())
    return a
    #stock_data_temp2.head()
    

    

