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
# the api retrieves the data and calculates the MSE,RMSE,SI for stock
@app.route("/api/GetMetrics/<ticker>")
def GetMetrics(ticker):
    import pandas as pd;
    # For time stamps
    from datetime import datetime, timedelta;
    print(ticker);
    import math;
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import mean_absolute_error
    import sklearn.metrics as metrics
    # Importing the statistics module 
    import statistics 
    
   
    #define function to calculate cv
    cv = lambda x: np.std(x, ddof=1) / np.mean(x) * 100;    

    # calculate performance statistics for GRU
    with open('Resources/output/GRUFinal.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',');
        first_line = True
        metric_data = [];

        results = filter(lambda row: row[0] == ticker, data)

        df = pd.DataFrame(results);
        #print(df)
        df[2] = df[2].astype(float)
        df[4] = df[4].replace(r'^\s*$', 0, regex=True)
        df[4] = df[4].astype(float)

        df[3] = df[3].replace(r'^\s*$', 0, regex=True)
        df[3] = df[3].astype(float);

        
        gruMSE = mean_squared_error(df[2], df[3]);
        gruRMSE = math.sqrt(gruMSE);
        gruNRMSE = gruRMSE /(statistics.mean(df[2]));
        gruMAE =  mean_absolute_error(df[2], df[3]);      
        gruR2 = metrics.r2_score(df[2],df[3]);

        gruMSELag = mean_squared_error(df[2], df[4]);
        gruRMSELag = math.sqrt(gruMSELag);
        gruNRMSELag = gruRMSELag /(statistics.mean(df[2]));
        gruMAELag =  mean_absolute_error(df[2], df[4]);      
        gruR2Lag = metrics.r2_score(df[2],df[4]);
    
    # calculate performance statistics for LSTM
    with open('Resources/output/LSTMFinal.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',');
        first_line = True
        metric_data = [];

        results = filter(lambda row: row[0] == ticker, data)

        df = pd.DataFrame(results);
        #print(df)
        df[2] = df[2].astype(float)
        df[4] = df[4].replace(r'^\s*$', 0, regex=True)
        df[4] = df[4].astype(float)

        df[3] = df[3].replace(r'^\s*$', 0, regex=True)
        df[3] = df[3].astype(float);

        lstmMSE = mean_squared_error(df[2], df[3]);
        lstmRMSE = math.sqrt(lstmMSE);
        lstmNRMSE = lstmRMSE /(statistics.mean(df[2]));
        lstmMAE =  mean_absolute_error(df[2], df[3]);      
        lstmR2 = metrics.r2_score(df[2],df[3]);

        lstmMSELag = mean_squared_error(df[2], df[4]);
        lstmRMSELag = math.sqrt(lstmMSELag);
        lstmNRMSELag = lstmRMSELag /(statistics.mean(df[2]));
        lstmMAELag =  mean_absolute_error(df[2], df[4]);      
        lstmR2Lag = metrics.r2_score(df[2],df[4]);
    
    #build data model

    statDict = {

        'lstmMSE' :  str("{0:.4f}".format(lstmMSE)),
        'lstmRMSE' : str("{0:.4f}".format(lstmRMSE)),
        'lstmNRMSE' : str("{0:.4f}".format(lstmNRMSE)),
        'lstmMAE' :  str("{0:.4f}".format(lstmMAE)),      
        'lstmR2' : str("{0:.4f}".format(lstmR2)),

        'lstmMSELag' : str("{0:.4f}".format(lstmMSELag)),
        'lstmRMSELag' : str("{0:.4f}".format(lstmRMSELag)),
        'lstmNRMSELag' : str("{0:.4f}".format(lstmNRMSELag)),
        'lstmMAELag' : str("{0:.4f}".format(lstmMAELag)),      
        'lstmR2Lag' : str("{0:.4f}".format(lstmR2Lag)),

        'gruMSE' :  str("{0:.4f}".format(gruMSE)),
        'gruRMSE' : str("{0:.4f}".format(gruRMSE)),
        'gruNRMSE' : str("{0:.4f}".format(gruNRMSE)),
        'gruMAE' :  str("{0:.4f}".format(gruMAE)),      
        'gruR2' : str("{0:.4f}".format(gruR2)),

        'gruMSELag' : str("{0:.4f}".format(gruMSELag)),
        'gruRMSELag' : str("{0:.4f}".format(gruRMSELag)),
        'gruNRMSELag' : str("{0:.4f}".format(gruNRMSELag)),
        'gruMAELag' : str("{0:.4f}".format(gruMAELag)),      
        'gruR2Lag' : str("{0:.4f}".format(gruR2Lag))

    }

    return jsonify(statDict)

    

       


            
    return jsonify(metric_data)
# end GetMetrics() route



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