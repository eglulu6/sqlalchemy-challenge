# import dependancies
import sqlalchemy
from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Database = automap_base( )

# reflect the tables
Database.prepare(engine, reflect=True)

# View all of the classes that automap found
Database.classes.keys( )

# Save references to each table 
Measuerement = Database.classes.measurement
Station = Database.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)
inspector = inspect(engine)

app = Flask(__name__)

##################################################################################################

# List all routes that are available.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#################################################################################################

# PAGE: /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def prcp():
    # start a new session
    session = Session(bind=engine)

    # STEP 1: Find the most recent date in the data set.
    earliest_date = session.query(Measuerement.date).order_by(Measuerement.date.desc()).first()

    # STEP 2: Calculate the date one year from the last date in data set.
    end_date = dt.datetime.strptime(earliest_date[0],'%Y-%m-%d') - dt.timedelta(days=365)

    # STEP 3: Perform a query to retrieve the data and precipitation scores
    prcp_12_mo_data = session.query(Measuerement.date, Measuerement.prcp).filter(Measuerement.date > end_date).all()
    
    session.close()

    # STEP 4: Save the query results as a Pandas DataFrame and set the index to the date column
    prcp_df = pd.DataFrame(prcp_12_mo_data, columns=['date', 'prcp'])

    # STEP 5: Sort the dataframe by date
    prcp_df.sort_values('date',ascending=False)

    # break the date into yr_mo for easier plotting
    yr_mo = []
    for date in prcp_df['date']:
        yr_mo.append(date[0:7])
    prcp_df['yr_mo'] = yr_mo

    # Convert the Exploratory Precipitation Analysis query results
    # to a dictionary using `date` as the key and `prcp` as the value.

    #empty list
    prcp_json_list = []

    # loop thru date & prcp in prcp_12_mo_data to pull into key : values
    for date, prcp in prcp_12_mo_data:
        prcp_dict = {date : prcp}

        # append into empty list
        prcp_json_list.append(prcp_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(prcp_json_list)

#################################################################################################

# PAGE:  /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    # start a new session
    session = Session(bind=engine)

    #empty list
    stataion_json_list = []

    #query table to get station names
    active_stations = session.query(Station.name).all()

    session.close()

    # loop thru date & prcp in prcp_12_mo_data to pull into key : values
    for name in active_stations:

        # append into empty list
        stataion_json_list.append(name)

# Return a JSON list of stations from the dataset.
    return jsonify(stataion_json_list)

#################################################################################################

# PAGE:   `/api/v1.0/tobs`
@app.route('/api/v1.0/tobs')
def date_tobs():
    # start a new session
    session = Session(bind=engine)

    # Design a query to find the most active stations (i.e. what stations have the most rows?)
    # List the stations and the counts in descending order.
    active_stations_count = engine.execute('SELECT station, COUNT(*) FROM measurement GROUP BY station ORDER BY count(*) DESC').fetchall()
    most_active_station = active_stations_count[0][0]

    # Query the dates and temperature observations of the most active station for the last year of data.
    most_active = session.query(Measuerement.date, Measuerement.tobs)\
    .filter(Measuerement.date > end_date)\
    .filter(Measuerement.station == most_active_station)

    session.close()

    #empty list
    most_active_stataion_json_list = []

    # loop thru date & prcp in most_active to pull into key : values
    for date, prcp in prcp_12_mo_data:
        prcp_dict = {date : prcp}

        # append into empty list
        most_active_stataion_json_list.append(prcp_dict)

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(most_active_stataion_json_list)

#################################################################################################

# PAGE: `/api/v1.0/<start>` 
@app.route('/api/v1.0/<start>')
def tobs_start_sumry(start):
    # start a new session
    session = Session(bind=engine)

# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    # JSON list of the minimum temperature, the average temperature, and the max temperature
    start = '2010-01-06'
    end = '2016-08-24'

    # Using the start and/or end date calculate the lowest, highest, and average temperature.
    # store values for print statement
    date_min_tobs = session.query(func.min(Measuerement.tobs)).\
        filter(Measuerement.date >= start).all()[0][0]

    date_max_tobs = session.query(func.max(Measuerement.tobs)).\
        filter(Measuerement.date >= start).all()[0][0]

    date_avg_tobs = round(session.query(func.avg(Measuerement.tobs)).\
        filter(Measuerement.date >= start).all()[0][0],2)

    session.close()

    #store values in dict for json
    date_summry_dict = {'Min_Temp': date_min_tobs, 'Max_Temp: ': date_max_tobs,'Avg_Temp: ': date_avg_tobs}

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(date_summry_dict)

#################################################################################################

# PAGE: `/api/v1.0/<start>/<end>`
@app.route('/api/v1.0/<start>/<end>')
def tobs_sumry(start, end):
    # start a new session
    session = Session(bind=engine)

# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    # JSON list of the minimum temperature, the average temperature, and the max temperature
    start = '2010-01-06'
    end = '2016-08-24'

    # Using the start and/or end date calculate the lowest temperature
    date_min_tobs = session.query(func.min(Measuerement.tobs))\
        .filter(Measuerement.date >= start)\
        .filter(Measuerement.date <= end)\
        .all()[0][0]
    # Using the start and/or end date calculate the highest temperature
    date_max_tobs = session.query(func.max(Measuerement.tobs))\
        .filter(Measuerement.date >= start)\
        .filter(Measuerement.date <= end)\
        .all()[0][0]
    # Using the start and/or end date calculate the average temperature
    date_avg_tobs = round(session.query(func.avg(Measuerement.tobs))\
        .filter(Measuerement.date >= start)\
        .filter(Measuerement.date <= end)\
        .all()[0][0],2)

    session.close()

    #store values in dict for json
    date_summry_dict = {'Min_Temp': date_min_tobs, 'Max_Temp: ': date_max_tobs,'Avg_Temp: ': date_avg_tobs}

# Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(date_summry_dict)

#################################################################################################


if __name__ == '__main__':
    app.run(debug=True)