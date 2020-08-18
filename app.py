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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
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
    highest_station = session.query(Measurement.date, Measurement.tobs).\
    filter(Station.id == 7).\
    filter(Station.station == Measurement.station).\
    filter(func.strftime(Measurement.date) >= firstdate).\
    order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into list - Not very easy to look at!
    highest_station_list = list(np.ravel(highest_station))

    # # Convert the query results to a dictionary to make the page easier to read...
    # highest_station_list = []

    # for date, tobs in highest_station:
    #     tobs_dict = {}
    #     tobs_dict['Date'] = date
    #     tobs_dict['TOBS'] = tobs
    #     highest_station_list.append(tobs_dict)

    return jsonify(highest_station_list)

# Define station route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>")
def start():
    # Create  session from Python to the DB
    session = Session(engine)




    session.close()




    return


# Define station route("/api/v1.0/<end>")
@app.route("/api/v1.0/<end>")
def end():
    # Create  session from Python to the DB
    session = Session(engine)




    session.close()



    
    return



if __name__ == "__main__":
    app.run(debug=True)