import logging 
import pandas as pd
import json
import sqlalchemy as db
from sqlalchemy import engine,create_engine

import pymysql
from sqlalchemy import MetaData,Table, Column, Integer, String,Float,DateTime
import warnings
import logging  
from funclist import sucess_fun,mysql_func
from executefunc import gettest,outputcount,sector_list_query

from flask import Flask,render_template,request,redirect, url_for,session,flash

app = Flask(__name__)
app.secret_key = "##44547466"



@app.route('/newyfcode')
def newyfcode():
    with mysql_func().connect() as conn:
        
        get_all_df=outputcount(conn)  #function outputcount
        sector_df=sector_list_query(conn) #function sector_list_query

        
        
    try:
        return render_template('newyfcode.html', tables=[get_all_df.to_html(index=False,classes=['df2'])], titles=['na','Company Yahoo Finance List'],sector_df=sector_df)
    except:
        flash(f"{sector_df}")
        return sector_df



@app.route('/newyfcodeupdate', methods=['GET', 'POST'])
def newyfcodeupdate():

    results = {}

    if request.method=='POST':

        company_name=request.form['company_name']
        company_code=request.form['company_code']
        company_sector=request.form['company_sector']
        stock_data=request.form['stock_data']
        
        with mysql_func().connect() as conn:

            check_code_query=f"select distinct company_code from company_code where company_code='{company_code}'"
            check_code_df=conn.execute(check_code_query).fetchone()
            
            print(check_code_df)

            if check_code_df is None:
                
                insert_query=f"insert into company_code(company_name,company_code,company_sector) values('{company_name}','{company_code}','{company_sector}')"
                conn.execute(insert_query)

                count_query="select count(*) from company_code"
                getcount=conn.execute(count_query).fetchone()[0]
                
                get_output=gettest(company_name,company_code,conn)
    
                flash(f"New record entered for {get_output}  : {getcount}")
            else:
                
                flash(f"{company_code} code already exists")

            conn.close()
            
    return redirect(url_for('newyfcode'))    

        
    



@app.route('/output')
def output():
     with mysql_func().connect() as conn:
        

        return render_template('output.html', dfs=[outputcount(conn).to_html(index=False,classes='df')], titles=['na','Complete list'])  #Calling function outputcount()
        conn.close()



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login',methods=['POST','GET'])
def login():
    

    if request.method=='POST':
        login_result=request.form
        username=login_result['username']
        password=login_result['password']

        with mysql_func().connect() as conn:
            result=conn.execute("select * from login_table where username=\'{}\' and password=\'{}\'".format(username,password))

            rows1=result.fetchone()
    
            if rows1:
                
                session['username'] = request.form.get('username')
                
                if 'username' in session:
                    username=session['username']

                #return redirect(url_for('home'))  #page2 is function name not html file name
                return render_template('home.html',sess_user=username)
                
            else:
                flash("incorrect username or password")
                return redirect(url_for('index'))   #home is function name not html file name





if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
    
    #app.run()



