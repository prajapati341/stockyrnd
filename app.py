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
    return render_template('newyfcode.html')



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
    app.run(debug=True,host='0.0.0.0')
    
    #app.run()


