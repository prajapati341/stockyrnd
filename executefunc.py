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
from tvDatafeed import TvDatafeed, Interval



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


def execute_yf_code(conn):    # Daywise extraction from YF


    max_query_day='''
      select company_name,company_code,concat(date(max(date)),' 00:00:00') max_date,date_add(date(max(date)),interval 1 day) start_date,date(now()) end_date  from stock_data  group by company_name,company_code;
      '''

    exec_df=pd.DataFrame(conn.execute(max_query_day))

    stock_data_temp1=pd.DataFrame()
    stock_data_temp2=pd.DataFrame()

    for i in range(len(exec_df)):

        # Day wise data extraction
        #-------------------------------------------------------------------------------

        stock_data_temp1=yf.download(exec_df.loc[i]['company_code'], exec_df.loc[i]['start_date'], exec_df.loc[i]['end_date'])

        stock_data_temp1['Company_Name']=exec_df.loc[i]['company_name']
        stock_data_temp1['Company_Code']=exec_df.loc[i]['company_code']
        stock_data_temp1=stock_data_temp1.reset_index()
        
        max_dt=exec_df.loc[i]['max_date']
        max_dt2=f"'{max_dt}'"
        stock_data_temp1=stock_data_temp1[stock_data_temp1['Date']>max_dt2]
        stock_data_temp2=pd.concat([stock_data_temp1,stock_data_temp2])
        
        
             
        #-------------------------------------------------------------------------------

    
    stock_data_temp2.to_sql('stock_data',con=conn,index=False,if_exists='append')  # 1 day interval  



    a=list(stock_data_temp2['Company_Code'].unique())  #list out all company code
    return a


def exec_yf_interval(conn):    #1 minute interval extraction from YF
    max_query_interval='''
                        select distinct company_name,company_code,max(datetime) max_date  from stock_data_interval  
                        group by company_name,company_code;
                        '''
    exec_df=pd.DataFrame(conn.execute(max_query_interval))
    stock_data_interval_temp1=pd.DataFrame()
    stock_data_interval_temp2=pd.DataFrame()

    for i in range(len(exec_df)):
        
        stock_data_interval_temp1=yf.download(exec_df.loc[i]['company_code'],interval="1m")

        stock_data_interval_temp1['Company_Name']=exec_df.loc[i]['company_name']
        stock_data_interval_temp1['Company_Code']=exec_df.loc[i]['company_code']

        
        stock_data_interval_temp1=stock_data_interval_temp1.reset_index()
        max_dt=exec_df.loc[i]['max_date']
        max_dt2=f"'{max_dt}'"
        stock_data_interval_temp1=stock_data_interval_temp1[stock_data_interval_temp1['Datetime']>max_dt2]

        stock_data_interval_temp2=pd.concat([stock_data_interval_temp1,stock_data_interval_temp2])
    

    stock_data_interval_temp2.to_sql('stock_data_interval',con=conn,index=False,if_exists='append')
    



def exec_interval(conn):
    try:
        with open('cred.json','r') as cred_file:
            cred=cred_file.read()
        obj=json.loads(cred)
        tv_user=obj['tv_user']
        tv_pwd=obj['tv_pwd']

        tv=TvDatafeed(tv_user,tv_pwd)
        
    except:
        return 'Problem while fetching data from Trading view'


    max_query_interval='''
                        select distinct company_name,company_code from stock_data
                        '''

    exec_interval_df=pd.DataFrame(conn.execute(max_query_interval))

    stock_data_interval_temp1=pd.DataFrame()
    stock_data_interval_temp2=pd.DataFrame()

    for i in range(len(exec_interval_df)):

        
        str1=exec_interval_df.loc[i]['company_code']
        cmp_code=str1.replace('.NS','')

        stock_data_interval_temp1 = tv.get_hist(symbol=cmp_code,exchange='NSE',interval=Interval.in_1_minute,n_bars=10000)

        stock_data_interval_temp1['Company_Name']=exec_interval_df.loc[i]['company_name']
        stock_data_interval_temp1['Company_Code']=f'{cmp_code}.NS'
        stock_data_interval_temp1['Adj Close']=stock_data_interval_temp1['close']
        stock_data_interval_temp1=stock_data_interval_temp1.reset_index()


        stock_data_interval_temp2=pd.concat([stock_data_interval_temp1,stock_data_interval_temp2])
        
        #-------------------------------------------------------------------------------

    stock_data_interval_temp2.rename(columns={'datetime':'Datetime','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'},inplace=True)
    stock_data_interval_temp2.drop(columns={'symbol'},inplace=True)

    stock_data_interval_temp2.to_sql('stock_data_interval',con=conn,index=False,if_exists='append')    #1 min interval

    


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


        query=f'''insert into user_portfolio values ({cust_id},'{buydate}','{stockname}',{quantity},{buyval},{buyprice},DATE('{selldate}'),{sellval},{sellprice},{totalcharges},{profitloss},'{status}')'''
        
        conn.execute(query)
        return 'updated new record'
    except :
        return selldate




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


def fetch_portfolio_list(conn,cust_id):
    try:
        query=f'''
        select * from user_portfolio where cust_id={cust_id} order by buy_date desc;
        '''
        portlist=conn.execute(query).fetchall()
        portlist=pd.DataFrame(portlist)
        return portlist
    except:
        print()
    
    
