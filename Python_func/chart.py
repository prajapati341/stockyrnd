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
            select distinct datetime as Datetime,open,high,low,close as Close,'Adj Close',volume,company_name,company_code from stock_data_interval  where company_code='^NSEI';
            '''
    indics_df=pd.DataFrame(conn.execute(query))

    indics_df=indics_df[(indics_df['Datetime']>='2023-02-01 00:00:00') & (indics_df['Datetime']<='2023-02-01 23:59:59')]

    indics_df['Days']=indics_df['Datetime'].dt.strftime('%d-%b')
    indics_df['Hour_Min']=indics_df['Datetime'].dt.strftime('%H:%M')
    title_name=indics_df['company_code'].unique()

    fig,ax=plt.subplots(figsize=(20,5))

    indics_df.pivot_table(index='Hour_Min',columns='Days',values='Close').plot(kind='line',ax=ax,rot=90)
    plt.title(title_name)

    plt.savefig('static/chart_img/default_chart1.png')


def create_chart(conn,stockname):
    print('create chart 2',stockname)
    query=f'''
            select distinct datetime as Datetime,open,high,low,close as Close,'Adj Close',volume,company_name,company_code from stock_data_interval  where company_code='{stockname}';
            '''
    indics_df=pd.DataFrame(conn.execute(query))

    indics_df=indics_df[(indics_df['Datetime']>='2023-02-01 00:00:00') & (indics_df['Datetime']<='2023-02-01 23:59:59')]

    indics_df['Days']=indics_df['Datetime'].dt.strftime('%d-%b')
    indics_df['Hour_Min']=indics_df['Datetime'].dt.strftime('%H:%M')
    title_name=indics_df['company_code'].unique()

    fig,ax=plt.subplots(figsize=(20,5))

    indics_df.pivot_table(index='Hour_Min',columns='Days',values='Close').plot(kind='line',ax=ax,rot=90)
    plt.title(title_name)

    plt.savefig('static/chart_img/selected_chart1.png')
    
    



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

 





    