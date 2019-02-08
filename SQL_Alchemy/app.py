import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

def calc_temps_1(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
def calc_temps_2(start_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

@app.route('/')
def home():
        print("Server received request for 'Home' page...")
        return "Availiable routes:  '/api/v1.0/precipitation'    '/api/v1.0/stations'    '/api/v1.0/tobs'    '/api/v1.0/<start>'    '/api/v1.0/<start_date>/<end_date>'"

@app.route('/api/v1.0/precipitation')
def precipitation():
    print("Server received request for 'precipitation' page...")
    last_12_months = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-23').\
            order_by(Measurement.date).all()
    df_12_mos = pd.DataFrame(last_12_months)
    df_12_mos = df_12_mos.set_index('date')
    df_12_mos = df_12_mos.dropna()
    df_12_mos = df_12_mos.sort_values('date', ascending=False)
    precip_dict = df_12_mos.to_dict()
    return jsonify(precip_dict['prcp'])

@app.route('/api/v1.0/stations')
def stations():
    print("Server received request for 'stations' page...")    
    stations_query = session.query(Measurement.station, Station.name).\
        filter(Measurement.station == Station.station).all()
    df_stations = pd.DataFrame(stations_query)
    df_stations = df_stations.set_index('station')
    df_stations = df_stations.dropna()
    stations_dict = df_stations.to_dict()
    return jsonify(stations_dict['name'])

@app.route('/api/v1.0/tobs')
def tobs():
    print("Server received request for 'tobs' page...")   
    last_12_months = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > '2016-08-23').\
        order_by(Measurement.date).all()
    df_12_mos = pd.DataFrame(last_12_months)
    df_12_mos = df_12_mos.set_index('date')
    df_12_mos = df_12_mos.dropna()
    tobs_dict = df_12_mos.to_dict()
    return jsonify(tobs_dict['tobs'])

@app.route('/api/v1.0/<start>')
def start_date(start):
    print("Server received request for '<start>' page...")
    response = calc_temps_2(start)
    return "Min Temp: " + str(response[0][0]) + ' ' + "Avg Temp: " + str(response[0][1]) + ' ' + "Max Temp: " + str(response[0][2])

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    print("Server received request for '<start>/<end>' page...")    
    response = calc_temps_1(start, end)
    return "Min Temp: " + str(response[0][0]) + ' ' + "Avg Temp: " + str(response[0][1]) + ' ' + "Max Temp: " + str(response[0][2])

if __name__ == "__main__":
    app.run(debug=True)
