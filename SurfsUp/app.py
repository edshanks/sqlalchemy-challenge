# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
def homepage():
    """viewing homepage and listing all routes"""
    
    print("Server received request for 'Homepage'.....")
    return(f"Available routes:</br>"
           f'</br>'
           f'precipitation data in the last year</br>'
           f"/api/v1.0/precipitation</br>"
           f'</br>'
           f'all stations</br>'
           f"/api/v1.0/stations</br>"
           f'</br>'
           f'all temperature observations from most active station in the last year</br>'
           f"/api/v1.0/tobs</br>"
           
       
           f'</br>'
           f'minimum, maximum, and average temperature recorded at most active station since specified start date</br>'
           f"/api/v1.0/start/<start></br>"
           f"example start link --- /api/v1.0/start/2011-05-16</br>"
           f'</br>'
           f'minimum, maximum, and average temperature recorded at most active station between specified start date and end date</br>'
           f"/api/v1.0/start/end/<start>/<end></br>"
           f"example start/end link --- /api/v1.0/start/end/2011-05-16/2012-05-16")

     
######################################################################################
    
@app.route("/api/v1.0/precipitation")
def precipitation():    
    """viewing precipiation data"""
    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    last_year = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= year_ago).\
        order_by(Measurement.date).all()
    
    
    
    prcp_list = []
    for date, prcp in last_year:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_list.append(prcp_dict)
        
    session.close()
    
    print("Server received request for precipitation data.....")
    return jsonify(prcp_list)
    
    

######################################################################################

@app.route("/api/v1.0/stations")
def stations():
    """viewing stations"""
    results = session.query(Station.name, Station.station).all()
    
    
    
    station_list = []
    
    for name, station in results:
        station_dict = {}
        station_dict['name'] = name
        station_dict['station'] = station
        station_list.append(station_dict)

    session.close()    
        
    print("Server received request for 'stations'.....")      
    return jsonify(station_list)

#########################################################################################

@app.route("/api/v1.0/tobs")
def tobs():
    """viewing all temperature data"""
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    result = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.station == 'USC00519281', Measurement.date >= year_ago)

    
    tobs_list = []
    for date, tobs in result:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_list.append(tobs_dict)
    
    session.close()
    
    print("Server received request for 'all temperature data'.....")
    return jsonify(tobs_list)

#########################################################################################

@app.route("/api/v1.0/start/<start>")
def start(start):
    """viewing temperature data with specified start date"""
    temp = Measurement.tobs

    min_max_avg = session.query(func.min(temp), func.max(temp), func.avg(temp))\
    .filter(Measurement.station == 'USC00519281', Measurement.date >= start)
    
    
    
    min_max_avg_start = []
    for mn, mx, av in min_max_avg:
        mn_mx_av = {}
        mn_mx_av['minimum temperature'] = mn
        mn_mx_av['maximum temperature'] = mx
        mn_mx_av['average temperature'] = av
        min_max_avg_start.append(mn_mx_av)
    
    session.close()
    
    print("Server received request for 'temperature data with specified start date'")
    return jsonify(min_max_avg_start)
    
###########################################################################################
@app.route("/api/v1.0/start/end/<start>/<end>")
def start_end(start, end):
    """viewing temperature data with specified start and end dates"""
    temp = Measurement.tobs

    min_max_avg_start_end = session.query(func.min(temp), func.max(temp), func.avg(temp))\
    .filter(Measurement.station == 'USC00519281', Measurement.date >= start, Measurement.date <= end)

    
    min_max_avg_start_end_list = []
        
    for mn, mx, av in min_max_avg_start_end:
        mn_mx_av_dict = {}
        mn_mx_av_dict['minimum temperature'] = mn
        mn_mx_av_dict['maximum temperature'] = mx
        mn_mx_av_dict['average temperature'] = av
        min_max_avg_start_end_list.append(mn_mx_av_dict)
    
    session.close()
    
    print("Server received request for 'temperature data with specified start and end dates'")
    return jsonify(min_max_avg_start_end_list)
    
if __name__ == '__main__':
    app.run(debug=True)