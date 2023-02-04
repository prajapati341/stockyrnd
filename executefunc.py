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
from datetime import datetime




def gettest(company_name,company_code,conn):

    try:
    
        start_date = '2023-01-21'
        end_date = '2023-01-31'
        
        #stock_data = yf.download(company_code, start_date, end_date)
        stock_data = yf.download(company_code)
        stock_data_interval_temp=yf.download(company_code,interval="1m")

        stock_data['Company_Name']=company_name
        stock_data['Company_Code']=company_code

        stock_data_interval_temp['Company_Name']=company_name
        stock_data_interval_temp['Company_Code']=company_code

        stock_data=stock_data.reset_index()
        stock_data_interval_temp=stock_data_interval_temp.reset_index()


        stock_data.to_sql('stock_data',con=conn,index=False,if_exists='append')

        stock_data_interval_temp.to_sql('stock_data_interval',con=conn,index=False,if_exists='append')

        return company_name
    except Exception as e:
        return e


def outputcount(conn):
    output_query='''
    select a.*,b.Records as 'Interval Records',b.Noofdays as 'Interval Days' from (
            select  b.cmp_code as 'CompanyDBID',a.company_name as 'Company Name',a.company_code as 'Company_Code',count(a.company_code) as Records,b.company_sector as 'Company Sector',date(min(a.Date)) as 'First Record',date(max(a.Date)) as 'Last Updated Record',datediff(max(a.Date),min(a.Date)) as 'No of days' from stock_data a
            left join company_code b on a.Company_Code=b.company_code
            group by b.cmp_code,a.company_name,a.company_code,b.company_sector
        ) a
            left join 
        (    

            select  b.cmp_code as 'CompanyDBID',a.company_name as 'Company Name',a.company_code as 'Company_Code',count(a.company_code) as Records,b.company_sector as 'Company Sector',date(min(a.datetime)) as 'First Record',date(max(a.datetime)) as 'Last Updated Record',datediff(max(a.datetime),min(a.datetime)) as 'Noofdays' from stock_data_interval a
            left join company_code b on a.Company_Code=b.company_code
            group by b.cmp_code,a.company_name,a.company_code,b.company_sector
        ) b on a.Company_Code=b.Company_Code
        order by a.CompanyDBID
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
      select company_name,company_code,date(max(date)) max_date,date_add(date(max(date)),interval 1 day) start_date,date(now()) end_date  from stock_data  group by company_name,company_code;
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
    a=list(stock_data_temp2['Company_Code'].unique())  #list out all company code
    return a

def portfolio_record(conn,cust_id,buydate,stockname,quantity,buyval,buyprice,selldate,sellval,sellprice,totalcharges,profitloss,status):
    try:
        if selldate =='':
            selldate=buydate
        
        if sellval=='':
            sellval=0

        if sellprice=='':
            sellprice=0
        
        if totalcharges=='':
            totalcharges=0

        if profitloss=='':
            profitloss=0

        if status=='':
            status='Active'
            
        #print(cust_id,buydate,stockname,quantity,buyval,buyprice,selldate,sellval,sellprice,totalcharges,profitloss,status)


        query=f'''insert into user_portfolio values ({cust_id},'{buydate}','{stockname}',{quantity},{buyval},{buyprice},'{selldate}',{sellval},{sellprice},{totalcharges},{profitloss},'{status}')'''
        
        conn.execute(query)
        return 'updated new record'
    except:
        return 'error while adding new record please check all fields'




def company_list(conn):
    try:

        query='''
            select distinct company_name,company_code from company_code;
        '''
        comp_code=conn.execute(query).fetchall()
        comp_code=pd.DataFrame(comp_code)
        comp_code=comp_code['company_code']
        return comp_code
    except:
        return 'error in company code function'

    
