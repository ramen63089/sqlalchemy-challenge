#Import required packages

import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Setup Database

engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect the database into a new model
Base = automap_base()

#Reflect tables from the database
Base.prepare(engine, reflect=True)

#Save references to tables from the database
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")

def precipitation():
    session=Session(engine)
    date = dt.datetime(2016, 8, 22)
    results = session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date > date).all()
    session.close
    all_prcp=list(np.ravel(results))
    dict={}
    for i in all_prcp:
        key=i[0]
        value=i[1]
        dict[key]=value
    return jsonify(dict)

@app.route("api/v1.0/stations")
def stations():
    session=Session(engine)
    results = session.query(Measurement.station).\
    distinct().all()
    all_stations=list(np.ravel(results))
    return jsonify(all_stations)
    session.close

@app.route("api/v1.0/tobs")
def tobs(): 
    session=Session(engine)
    date = dt.datetime(2016, 8, 22)
    results = session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.date > date).\
    filter(Measurement.station == "USC00519281").all()
    session.close
    all_tobs=[]
    for tobs, date in results:
        dict = {}
        dict["tobs"] = tobs
        dict["date"] = date
        all_tobs.append(dict)
    return jsonify(all_tobs)

@app.route("api/v1.0/<start>")
def calc_temps(start_date):
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    session.close  
    all_tobs=[]
    for min, avg, max in results:
        dict = {}
        dict["min"] = min
        dict["avg"] = avg
        dict["max"] = max
        all_tobs.append(dict)
    return jsonify(all_tobs)


@app.route("api/v1.0/<start>/<end>")
def calc_temps(start_date, end_date):
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close 
    all_tobs=[]
    for min, avg, max in results:
        dict = {}
        dict["min"] = min
        dict["avg"] = avg
        dict["mxax"] = max
        all_tobs.append(dict)
    return jsonify(all_tobs)
