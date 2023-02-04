import logging 
import pandas as pd
import json
import sqlalchemy as db
from sqlalchemy import engine,create_engine

import pymysql
from sqlalchemy import MetaData,Table, Column, Integer, String,Float,DateTime
import warnings
import logging  
from flask import Flask,render_template,request,redirect, url_for,session,flash

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

        print('\n\n Cred file loaded')

    except Exception as json_file:
        print('credential file error ',json_file)
    
    try:
        
        pymysql.install_as_MySQLdb()

        engine = create_engine(f"mysql://{user}:{pwd}@{host}/{database}",echo = False)
        print('Database connection successful')
        str='connected'
        return engine
        
        

    except Exception as conn_err:

        print('connection error :',conn_err)


def pwd_check(conn,username,password):

    #Checking credentials
    result=conn.execute("select * from login_table where username=\'{}\' and password=\'{}\'".format(username,password))

    rows1=result.fetchone()
    

    if rows1:
        session['fullname']=rows1[1]   #Set username from fetchone in tuple form
        session['cust_id']=rows1[0]

        if 'fullname' in session:
            fullname=session['fullname']
            cust_id=session['cust_id']
            pass_str=['yes',fullname,cust_id]
            print('successful')
            
            return pass_str
    else:
        print('invalid')
        return 'invalid'


def session_logout():

    if session['fullname'] is None:
        return True
    else:
        return False
    print('Logout Now')        