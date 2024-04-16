# Import the dependencies.
import pandas as pd
import numpy as np
import datetime as dt
import re

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
from sqlalchemy import create_engine
db_path = 'sqlite:///C:/Users/Karamjit/Downloads/hawaii.sqlite'
engine = create_engine(db_path)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def main():
    return (
        f"Greetings to the API Homepage!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (Please use YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (Please use YYYY-MM-DD)"

    )

@app.route("/api/v1.0/precipitation")
def percipitation():
    session = Session(engine)
    one_year_prior = dt.date(2017, 8, 23)-dt.timedelta(365)
    percipitation_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_prior).all()
    percipitation = {date:prcp for date, prcp in percipitation_query}  
    return jsonify(percipitation)  

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    station_query = session.query(Station.station).all()
    stations_list = list(np.ravel(station_query))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_query = session.query(Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date>='2016-08-23').all()
    temprature_list = list(np.ravel(tobs_query))
    return jsonify(temprature_list)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    min_max_avg_query = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).all()
    stat_list = list(np.ravel(min_max_avg_query))
    return jsonify(stat_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    min_max_avg_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    stat_list = list(np.ravel(min_max_avg_query))
    return jsonify(stat_list)

if __name__ == '__main__':
    app.run(debug=True)