import logging 
import pandas as pd
import json
import sqlalchemy as db
from sqlalchemy import engine,create_engine

import pymysql
from sqlalchemy import MetaData,Table, Column, Integer, String,Float,DateTime
import warnings
import logging  

def sucess_fun():
    print('welcome from function')


def mysql_func():
    try:
        with open('cred.json','r') as cred_file:
            cred=cred_file.read()

        obj=json.loads(cred)
        user=obj['user']
        pwd=obj['pwd']
        host=obj['host']
        database=obj['database']

        print('\n\n JSON file loaded')

    except Exception as json_file:
        print('credential file error ',json_file)
    
    try:
        
        pymysql.install_as_MySQLdb()

        engine = create_engine(f"mysql://{user}:{pwd}@{host}/{database}",echo = True)
        print('connected successful')
        str='connected'
        return engine
        
        

    except Exception as conn_err:

        print('connection error :',conn_err)


def session_logout():
    print('Logout Now')        