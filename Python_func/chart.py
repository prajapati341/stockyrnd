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

def indics_chart(conn):
    query='''
            select distinct datetime as Datetime,open,high,low,close as Close,'Adj Close',volume,company_name,company_code from stock_data_interval  where company_code='TATAMOTORS.NS';
            '''
    indics_df=pd.DataFrame(conn.execute(query))

    indics_df=indics_df[(indics_df['Datetime']>='2023-02-01 00:00:00') & (indics_df['Datetime']<='2023-02-01 23:59:59')]

    indics_df['Days']=indics_df['Datetime'].dt.strftime('%d-%b')
    indics_df['Hour_Min']=indics_df['Datetime'].dt.strftime('%H:%M')

    fig,ax=plt.subplots(figsize=(20,5))


    indics_df.pivot_table(index='Hour_Min',columns='Days',values='Close').plot(kind='line',ax=ax,rot=90)

    get_img=plt.savefig('images/chart_img/test.png')
    
    sql_insert_blob_query = """ INSERT INTO user_chart_img
                          (chart_image, users_id, users_name) VALUES (%s,%s,%s,%s)"""
    conn.execute(sql_insert_blob_query, (get_img,1111,'sanjay'))

    #plt.show()

def fetch_img(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData







    