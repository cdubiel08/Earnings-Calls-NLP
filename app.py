# import necessary libraries
import os
import numpy as np
import datetime
import psycopg2
from sqlalchemy import cast, Date

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
if __name__ == "__main__":
    app.run(debug=True)
#################################################