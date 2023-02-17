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
from executefunc import gettest,outputcount,sector_list_query,execute_yf_code,portfolio_record,company_list,fetch_portfolio_list,exec_interval,exec_yf_interval

from flask import Flask,render_template,request,redirect, url_for,session,flash

app = Flask(__name__)
app.secret_key = "##44547466"


@app.route('/portfolio')
def portfolio():

    if session.get('fullname'):
        cust_id=session.get('cust_id')
        with mysql_func().connect() as conn:
            comp_code=company_list(conn)
            portlist=fetch_portfolio_list(conn,cust_id)
            portlist_len=len(portlist)
        conn.close()

        return render_template('portfoliohome.html',comp_code=comp_code,portlist=portlist,portlist_len=portlist_len)
    else:
        return redirect("/")

@app.route('/portfolio/edit',methods=['GET','POST'])        
def portfolio_edit():
    if session.get('fullname'):
        return render_template('portfolioedit.html')
    else:
        return redirect("/")


@app.route('/portfolio_add',methods=['GET', 'POST'])
def portfolio_add():
    if session.get('fullname'):
    
        if request.method=="POST":
            buydate=request.form.get('buydate')
            stockname=request.form.get('stockname')
            quantity=request.form.get('quantity')
            buyval=request.form.get('buyval')
            buyprice=request.form.get('buyprice')
            selldate=request.form.get('selldate')
            sellval=request.form.get('sellval')
            sellprice=request.form.get('sellprice')
            totalcharges=request.form.get('totalcharges')
            profitloss=request.form.get('profitloss')
            status=request.form.get('status')
            cust_id=session['cust_id']

            with mysql_func().connect() as conn:
                msg=portfolio_record(conn,cust_id,buydate,stockname,quantity,buyval,buyprice,selldate,sellval,sellprice,totalcharges,profitloss,status)
                flash(msg)

        return redirect("/portfolio")   
    
    else:

        return redirect("/")


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
                #newyfcodeupdate(conn,company_name,company_code,company_sector)

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

@app.route('/execute_output')
def execute_output():

    with mysql_func().connect() as conn:
        msg=execute_yf_code(conn)
        flash(msg)
        conn.close()
        return redirect(url_for('execute'))


@app.route('/execute_interval')
def execute_interval():

    with mysql_func().connect() as conn:
        msg=exec_interval(conn)
        flash(msg)
        conn.close()
        return redirect(url_for('execute'))

@app.route('/execute_yf_interval')
def execute_yf_interval():

    with mysql_func().connect() as conn:
        msg=exec_yf_interval(conn)
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
                return redirect(url_for('portfolio'))

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



