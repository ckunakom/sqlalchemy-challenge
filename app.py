# Import all the modules needed
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup

# Create an engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app. Pass __name__
app = Flask(__name__)

#################################################
# Flask Setup & Routes

# Calculate the date 1 year ago from the last data point in the database
firstdate = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Define index route - listing all routes
@app.route("/")
def home():
    return (
        f"Welcome to API for climate in Honolulu, Hawaii!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Replace 'start' and 'end' with YYYY-MM-DD<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# Define precipitation route("/api/v1.0/precipitation")
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create  session from Python to the DB
    session = Session(engine)

    # Query to retrieve the data and precipitation scores
    rain_data = session.query(Measurement.date, Measurement.prcp).\
    filter(func.strftime(Measurement.date) >= firstdate).all()

    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    date_prcp = []

    for date, prcp in rain_data:
        rain_dict = {}
        rain_dict['Date'] = date
        rain_dict['Precipitation'] = prcp
        date_prcp.append(rain_dict)

    return jsonify(date_prcp)

# Define station route("/api/v1.0/stations")
@app.route("/api/v1.0/stations")
def stations():
    # Create  session from Python to the DB
    session = Session(engine)

    # Query a list of stations from the dataset.
    station = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into list
    station_list = list(np.ravel(station))

    return jsonify(station_list)

# Define station route("/api/v1.0/tobs")
@app.route("/api/v1.0/tobs")
def tobs():
    # Create  session from Python to the DB
    session = Session(engine)

    # Query dates and temperature observations of the most active station for the last year of data.
    highest_station = session.query(Measurement.tobs).\
    filter(Station.id == 7).\
    filter(Station.station == Measurement.station).\
    filter(func.strftime(Measurement.date) >= firstdate).\
    order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into list
    highest_station_list = list(np.ravel(highest_station))

    return jsonify(highest_station_list)

# Define station route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>")
def date(start):

    # Create  session from Python to the DB
    session = Session(engine)
   
    # Query list of the minimum temperature, the average temperature, and the max temperature for a given start date
    tobs_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(func.strftime(Measurement.date) >= start).\
    group_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into list - Not very easy to look at!
    min_avg_max_list = list(np.ravel(tobs_temp))

    return jsonify(min_avg_max_list)


# Define station route("/api/v1.0/<start>/<end>")
@app.route("/api/v1.0/<start>/<end>")
def date_start_end(start, end):

    # Create  session from Python to the DB
    session = Session(engine)

    # Query list of the minimum temperature, the average temperature, and the max temperature for a given start date
    tobs_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(func.strftime(Measurement.date) >= start).filter(Measurement.date <= end).\
    group_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into list - Not very easy to look at!
    min_avg_max_list = list(np.ravel(tobs_temp))

    return jsonify(min_avg_max_list)

# The End.
if __name__ == "__main__":
    app.run(debug=True)