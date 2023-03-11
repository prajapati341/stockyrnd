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
import matplotlib.pyplot as plt
import base64
from PIL import Image
import io
 

def indics_chart(conn):
    query='''
            select distinct datetime as Datetime,open,high,low,close as Close,'Adj Close',volume,company_name,company_code from stock_data_interval  
            where company_code='^NSEI'
            and datetime>=concat(date(date_add(now(),interval -2 day)),' 00:00:00');
            '''
    indics_df=pd.DataFrame(conn.execute(query))

    #indics_df=indics_df[indics_df['Datetime']>=indics_df['Datetime'].max().strftime('%Y-%m-%d')+' 00:00:00']

    indics_df['Days']=indics_df['Datetime'].dt.strftime('%d-%b')
    indics_df['Hour_Min']=indics_df['Datetime'].dt.strftime('%H:%M')
    title_name=indics_df['company_code'].unique()

    fig,ax=plt.subplots(figsize=(20,5))

    indics_df.pivot_table(index='Hour_Min',columns='Days',values='Close').plot(kind='line',ax=ax,rot=90)
    plt.title(title_name)

    plt.savefig('static/chart_img/default_chart1.png')


def create_chart(conn,stockname,max_val,min_val):
    #print('create chart 2',stockname)


    query=f'''
            select distinct datetime as Datetime,open,high,low,close as Close,'Adj Close',volume,company_name,company_code from stock_data_interval  
            where datetime>=concat(date(date_add(now(),interval -5 day)),' 00:00:00')
            and company_code='{stockname}';
            '''
    indics_df=pd.DataFrame(conn.execute(query))

    #indics_df=indics_df[(indics_df['Datetime']>='2023-02-21 00:00:00') & (indics_df['Datetime']<='2023-02-24 23:59:59')]

    indics_df['Days']=indics_df['Datetime'].dt.strftime('%d-%b')
    indics_df['Hour_Min']=indics_df['Datetime'].dt.strftime('%H:%M')
    title_name=indics_df['company_code'].unique()


    df3=indics_df.copy()
    df3=indics_df.reset_index(drop=True)
    df3.head()
    df4=df3.groupby('Days').agg({'Close':['max','min']}).reset_index()
    df4.columns=df4.columns.droplevel(0)

    df3['Normalized']=''

    for a in range(len(df4)):
        
        for i in range(len(df3)):
            
            if df3.loc[i]['Days']==df4.loc[a]['']:
                df3.loc[i,['Normalized']]=float((df3.loc[i]['Close']-df4.loc[a]['min'])/(df4.loc[a]['max']-df4.loc[a]['min'])*100)
                #print(df3['Days'])

    fig,ax=plt.subplots(figsize=(20,5))
    df3.to_excel('/home/sanjay/Flask_Web/myFlaskApp/dump/df3.xlsx')
    df3.pivot_table(index='Hour_Min',columns='Days',values='Normalized').plot(kind='line',ax=ax,rot=90)
    
    plt.title(title_name+' [Normalized]')
    plt.savefig('static/chart_img/selected_chart1.png')



    fig,ax=plt.subplots(figsize=(20,5))

    
    
    
    try:
        
        stock_df=indics_df[indics_df['Datetime']>=datetime.today().strftime('%Y-%m-%d')+' 00:00:00']
        stock_df.pivot_table(index='Hour_Min',columns='Days',values='Close').plot(kind='line',ax=ax,rot=90)
        if max_val!='' or min_val!='':
            
            plt.axhline(y = float(max_val),color='r')
            plt.axhline(y = float(min_val),color='g')
        else:
            plt.axhline(y = float(stock_df['Close'].max()),color='r')
            plt.axhline(y = float(stock_df['Close'].min()),color='green')

        plt.title(title_name)
        plt.savefig('static/chart_img/selected_chart2.png')
    except:
        
        stock_df=indics_df[indics_df['Datetime']>=df3['Datetime'].max().strftime('%Y-%m-%d')+' 00:00:00']
        stock_df.pivot_table(index='Hour_Min',columns='Days',values='Close').plot(kind='line',ax=ax,rot=90)
        if max_val!='' or min_val!='':
            
            plt.axhline(y = float(max_val),color='r')
            plt.axhline(y = float(min_val),color='g')
        else:
            plt.axhline(y = float(stock_df['Close'].max()),color='r')
            plt.axhline(y = float(stock_df['Close'].min()),color='green')

        plt.title(title_name)
        plt.savefig('static/chart_img/selected_chart2.png')
    
    



#     first_profile_picture = convert_data('images/chart_img/test.jpg')

#     sql_insert_blob_query = """ INSERT INTO user_chart_img
#                           (chart_image, users_id, users_name) VALUES (%s,%s,%s)"""
#     result=conn.execute(sql_insert_blob_query, (first_profile_picture,1111,'sanjay'))


#     #Reading Image file
#     query2='''
#         SELECT chart_image FROM user_chart_img WHERE image_id=5;
# '''
#     df=conn.execute(query2)

#     data2 = df.fetchall()

#     file_like2 = io.BytesIO(data2[0][0])

#     img1=Image.open(file_like2)
#     return img1

    

def convert_data(file_name):
    with open(file_name, 'rb') as file:
        binary_data = file.read()
    return binary_data

 

def stock_refresh_for_chart(conn,stockname,max_val,min_val):         # Refresh NSE & Specific stock
    max_query_interval=f'''
                        select distinct company_name,company_code,max(datetime) max_date  from stock_data_interval
                        where company_code in ('^NSEI','{stockname}')
                        group by company_name,company_code
                       '''
    print(max_query_interval)
    print(stockname)
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
    
    create_chart(conn,stockname,max_val,min_val)



    