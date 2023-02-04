import logging 
import pandas as pd
import json
import sqlalchemy as db
from sqlalchemy import engine,create_engine

import pymysql
from sqlalchemy import MetaData,Table, Column, Integer, String,Float,DateTime

import warnings
import logging  
from funclist import sucess_fun,mysql_func,pwd_check,session_logout
from executefunc import gettest,outputcount,sector_list_query,execute_yf_code

from flask import Flask,render_template,request,redirect, url_for,session,flash

app = Flask(__name__)
app.secret_key = "##44547466"


@app.route('/portfolio')
def portfolio():
    return render_template('portfoliohome.html')


@app.route('/portfolio_add',methods=['GET', 'POST'])
def portfolio_add():
    if request.method=="POST":
        buydate=request.form.get('buydate')
        stockname=request.form.get('stockname')

        msg='{}{}'.format(buydate,stockname)
        return msg

    return render_template('portfoliohome.html')    
        
    
    
    

        # if buydate is None:
        #     return render_template('portfoliohome.html')
        # else:
        #     return '''<script>alert('hello')</script>'''

    #return redirect("/portfolio")


@app.route('/newyfcode')
def newyfcode():
    if session.get("fullname"):
        print('logged in ')
        with mysql_func().connect() as conn:
            get_all_df=outputcount(conn)  #function outputcount
            sector_df=sector_list_query(conn) #function sector_list_query for drop_down
        conn.close()

            
            
        try:
            return render_template('newyfcode.html', tables=[get_all_df.to_html(index=False,classes=['df2'])], titles=['na','Company Yahoo Finance List'],sector_df=sector_df)

            
        except:
            flash(f"{sector_df}")
            return sector_df
    else:

        return redirect("/")



@app.route('/newyfcodeupdate', methods=['GET', 'POST'])
def newyfcodeupdate():

    if session.get("fullname"):

        results = {}

        if request.method=='POST':

            company_name=request.form['company_name']
            company_code=request.form['company_code']
            company_sector=request.form['company_sector']
            stock_data=request.form['stock_data']
            
            with mysql_func().connect() as conn:
                newyfcodeupdate(conn,company_name,company_code,company_sector)

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
    else:
        return redirect("/") 

        
    



@app.route('/output')
def output():
    if session.get("fullname"):
        with mysql_func().connect() as conn:
            output_df=outputcount(conn)
            output_df_len=len(output_df)
            conn.close()

            return render_template('output.html', dfs=output_df,len=output_df_len)  #Calling function outputcount()
    else:

        return redirect("/")
        







@app.route('/execute')
def execute():
    if session.get("fullname"):
        with mysql_func().connect() as conn:
            output_df=outputcount(conn)
            output_df_len=len(output_df)
            conn.close()

            return render_template('execute.html', dfs=output_df,len=output_df_len)  #Calling function outputcount()
    else:
        return redirect("/")

@app.route('/execute_output', methods=['GET', 'POST'])
def execute_output():

    with mysql_func().connect() as conn:
        msg=execute_yf_code(conn)
        flash(msg)
        conn.close()
        
        
        return redirect(url_for('execute'))






@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home',methods=['POST','GET'])
def home():
    return render_template('home.html')


@app.route('/login_check',methods=['POST','GET'])
def login_check():
    

    if request.method=='POST':
        login_result=request.form
        username=login_result['username']
        password=login_result['password']


        with mysql_func().connect() as conn:
            str1=pwd_check(conn,username,password)
            #print(str1)
            
            
            if str1[0]=='yes':
                return redirect(url_for('home'))

            else:
                flash("incorrect username or password")
                return redirect(url_for('index'))   #home is function name not html file name
            



@app.route('/logout')    
def logout():
    session['fullname']=None
    #return render_template('index.html')
    return redirect("/")



if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
    
    #app.run()



