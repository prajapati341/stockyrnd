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

from flask import Flask,render_template,request,redirect, url_for,session,flash

app = Flask(__name__)
app.secret_key = "##44547466"



@app.route('/newyfcode')
def newyfcode():
    with mysql_func().connect() as conn:
        select_all_query="select company_name ,company_code,company_sector from company_code order by cmp_code desc"
        get_all_df=conn.execute(select_all_query)
        get_all_df=pd.DataFrame(get_all_df)

        select_sector_query="select sector from sector"
        sector_df=conn.execute(select_sector_query).fetchall()
        sector_df=pd.DataFrame(sector_df)
        sector_df=sector_df['sector']
        #print(sector_df)

    return render_template('newyfcode.html', tables=[get_all_df.to_html(index=False)], titles=[''],sector_df=sector_df)


@app.route('/newyfcodeupdate', methods=['GET', 'POST'])
def newyfcodeupdate():
    results = {}

    if request.method=='POST':
        company_name=request.form['company_name']
        company_code=request.form['company_code']
        company_sector=request.form['company_sector']
        #r=results.get(company_sector)
        #print(r)

        with mysql_func().connect() as conn:
            insert_query=f"insert into company_code(company_name,company_code,company_sector) values('{company_name}','{company_code}','{company_sector}')"
            conn.execute(insert_query)

            count_query="select count(*) from company_code"
            getcount=conn.execute(count_query).fetchone()[0]
            
            


            flash(f"Insert new record :  {company_name}  : {getcount}")
            
            conn.close()
            #return getcount
            return redirect(url_for('newyfcode'))    

        

        
    #return 'submited'
    



@app.route('/output')
def output():
     with mysql_func().connect() as conn:
        result=conn.execute("select * from stock_data")
        df=pd.DataFrame(result)
        

        return render_template('output.html', tables=[df.to_html(index=False)], titles=[''])



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
                
                session["username"] = request.form.get("username")

                return redirect(url_for('home'))  #page2 is function name not html file name
                
            else:
                flash("incorrect username or password")
                return redirect(url_for('index'))   #home is function name not html file name





if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
    
    #app.run()



