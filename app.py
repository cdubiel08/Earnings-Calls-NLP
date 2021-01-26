# import necessary libraries
import os
import numpy as np
import datetime
import psycopg2
from sqlalchemy import cast, Date
import csv

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from sqlalchemy.orm import aliased

# Postgres database user and password import
from db_key import user, password

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# create route that renders index.html template

@app.route("/")
def home():
    return render_template("index.html");
# end home() route

#################################################
# add the routes for the dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html");
## end dashboard() route

#################################################
# add the routes for the NLP
@app.route("/nlp")
def NLP():
    return render_template("nlp.html");
## end NLP() route


#################################################
# add the routes for the Forecast
@app.route("/forecast")
def Forecast():
    return render_template("forecast.html");
## end Forecast() route

#################################################
# add the routes for the Design
@app.route("/design")
def Design():
    return render_template("design.html");
## end Design() route

# add the routes for the Design
@app.route("/test")
def test():
    return render_template("index2.html");
## end Design() route


#################################################
# the api retrieves the companies list 
@app.route("/api/GetCompanyList")
def GetCompanyList():

    with open('Resources/input/companylist.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',');
        first_line = True
        company_data = [];
        for row in data:
            if not first_line:
                dict = {                
                    "Ticker": row[0],
                    "Company": row[1]             
                }
                company_data.append (dict)
            else:
                first_line = False

    return jsonify(company_data)
# end company_data() route

#################################################
# the api retrieves the LSTM data from the csv sends the json values
@app.route("/api/GetLSTMData/<ticker>")
def GetLSTMData(ticker):

    with open('Resources/output/LSTMFinal.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',');
        first_line = True
        lstm_data = [];

        results = filter(lambda row: row[0] == ticker, data)

        for row in results:
            if not first_line:
                dict = {                
                    "Ticker": row[0],
                    "Date": row[1],
                    "Actual": row[2],
                    "Pred": row[3],
                    "PredLag" : row[4]                                 
                }
                lstm_data.append (dict)
            else:
                first_line = False

    return jsonify(lstm_data)
# end lstm_data() route

#################################################
# the api retrieves the LSTM data from the csv sends the json values
@app.route("/api/GetGRUData/<ticker>")
def GetGRUData(ticker):

    with open('Resources/output/GRUFinal.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',');
        first_line = True
        lstm_data = [];

        results = filter(lambda row: row[0] == ticker, data)

        for row in results:
            if not first_line:
                dict = {                
                    "Ticker": row[0],
                    "Date": row[1],
                    "Actual": row[2],
                    "Pred": row[3],
                    "PredLag" : row[4]                                 
                }
                lstm_data.append (dict)
            else:
                first_line = False

    return jsonify(lstm_data)
# end GRU_data() route



#################################################
# the api retrieves the data and calculates the averages for stock
@app.route("/api/GetRollingAverages/<ticker>")
def GetRollingAverages(ticker):
    import pandas as pd;
    # For time stamps
    from datetime import datetime, timedelta;
    print(ticker);
    import math;

    with open('Resources/combined_top_25.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',');
        lstm_data = [];

        results = filter(lambda row: (row[1] == ticker) , data);
      
        df = pd.DataFrame(results);
        print(df)
        exp1 = df[3].ewm(span=20, adjust=False).mean();
        rolling_mean = df[3].rolling(window=20).mean();
        df[2] = df[2].astype(float)
        changepercent = df[2].pct_change();
       

        df['rolling_mean'] = rolling_mean;
        df['exp1'] = exp1;
        df['EReturn'] = changepercent;
        df['mean'] = changepercent.mean();
        df['std'] = changepercent.std();
        df =  df.dropna();
        for i, row in df.iterrows():
            

                dict = {                
                    "Ticker": row[1],
                    "Date": row[0],
                    "Close": row[3],
                    "MA": row['rolling_mean'],
                    "EMA" : row['exp1'] ,
                    "ER" : row['EReturn'],
                    "mean" : row['mean'],
                    "std"  : row ['std']                              
                }
                lstm_data.append (dict)
            
    return jsonify(lstm_data)
# end GRU_data() route


#################################################
# the api retrieves the stock data from the web and stores them in csv
@app.route("/api/GetStockData")
def GetStockData():
    import pandas as pd;
    from pprint import pprint;
    with open('Resources/today.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',');
        print('first')
        first_line = True
        stock_overview_data = [];
        
        #results = filter(lambda row: row[1] == ticker, data)
        
        for row in data:
            if not first_line:
                print('inside')

                df = pd.DataFrame({
                    "ticker" : row[1],
                    "52 Week Range" : row[6],
                    "Market Cap" : row[7],
                    "PE Ratio" : row[8],
                    "EPS" : row[9],
                    "Earnings Date": row[10] ,
                    "Dividend Rate" : row[11]
                }, index=[0]);
                metrics_fact_table = df.to_html( classes="table table-striped")

                dict = {                
                    "Ticker": row[1],
                    "Name": row[2],
                    "Open": row[3],
                    "Close": row[4],
                    "Volume" : row[5],
                    "Metrics" : metrics_fact_table,
                    "ShortTerm" :row[12],
                    "MiddleTerm" :row[13],
                    "LongTerm" : row[14]                    
                }
                stock_overview_data.append (dict)
            else:
                first_line = False

    return jsonify(stock_overview_data)
# end stock_overview_data() route
#################################################
if __name__ == "__main__":
    app.run(debug=True)
#################################################