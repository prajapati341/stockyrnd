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
# Set the start and end date



def gettest(company_name,company_code,conn):
    
    start_date = '2023-01-21'
    end_date = '2023-01-31'
    
    stock_data = yf.download(company_code, start_date, end_date)
    #stock_data = yf.download(company_code)

    stock_data['Company_Name']=company_name
    stock_data['Company_Code']=company_code

    stock_data=stock_data.reset_index()
    stock_data.to_sql('stock_data',con=conn,index=False,if_exists='append')

    return company_name


def test_func(check_code_df):
    return 'hello world'
