# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, cast

import numpy as np
import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C://Users//mrrit//OneDrive//Documents//UofO Data Class//Wk10_SQL_Adv//sqlalchemy-challenge//Starter_Code//Resources//hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
most_recent_date = dt.date(2017, 8, 23)
year_ago = most_recent_date - dt.timedelta(days=365)


@app.route("/")
def welcome():
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
    
    date = Measurement.date
    year_of_rain_data = session.query(date, Measurement.prcp)\
    .filter(date >= year_ago, date <= most_recent_date).all()

    session.close()

    precipitation_levels = []
    for date, prcp in year_of_rain_data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        precipitation_levels.append(precipitation_dict)

    return jsonify(precipitation_levels)

@app.route("/api/v1.0/stations")
def stations():
    station_column = Station.station
    active_stations = session.query(station_column)

    session.close()

    station_list = []
    for station in active_stations:
        station_list.append(station)

    station_list = list(np.ravel(station_list))    
    return jsonify(station_list)



@app.route("/api/v1.0/tobs")
def temperature():
    station_row = Measurement.station
    temperature = Measurement.tobs
    date = Measurement.date

    active_stations = session.query(station_row, func.count(station_row))\
    .group_by(station_row)\
    .order_by(func.count(station_row).desc()).all()
    
    most_active_station = active_stations[0][0]

    year_of_temp_data = session.query(date, temperature)\
    .filter(station_row == most_active_station)\
    .filter(date >= year_ago, date <= most_recent_date).all()

    session.close()

    temp_list = []
    for temp in year_of_temp_data:
        temp_list.append(temp)

    temp_list = list(np.ravel(temp_list))
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def temperature_range_1(start):
    date = Measurement.date
    temperature = Measurement.tobs
    
    range_of_temp_data = session.query(date, temperature)\
    .filter(date >= start, date <= most_recent_date).all()

    session.close()

    temp_range_list = []
    for temp in range_of_temp_data:
        temp_range_list.append(temp)

    temp_range_list = list(np.ravel(temp_range_list))
    return jsonify(temp_range_list)

@app.route("/api/v1.0/<start>/<end>")
def temperature_range_2(start, end):
    date = Measurement.date
    temperature = Measurement.tobs
    
    range_of_temp_data = session.query(date, temperature)\
    .filter(date >= start, date <= end).all()

    session.close()

    temp_range_list2 = []
    for temp in range_of_temp_data:
        temp_range_list2.append(temp)

    temp_range_list2 = list(np.ravel(temp_range_list2))
    return jsonify(temp_range_list2)

if __name__ == '__main__':
    app.run(debug=True)
