import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
def home():
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
def precip():
    """Getting precipitation data"""
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    """Preparing data"""
    precipitation = []
    for date, prcp in results:
        prcp_dict={}
        prcp_dict['date']=date
        prcp_dict['prcp']=prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    """Getting precipitation data"""
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    """Preparing data"""
    station = []
    for sta, name, lat, lng, el in results:
        sta_dict={}
        sta_dict['station']=sta
        sta_dict['name']=name
        sta_dict['location']={}
        sta_dict['location']['latitude']=lat
        sta_dict['location']['longitude']=lng
        sta_dict['location']['elevation']=el
        station.append(sta_dict)

    return jsonify(station)


@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)
    """Getting year info from data"""
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = np.ravel(last_date)
    date = last_date[0].split('-')
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    format_date = dt.date(year, month, day)
    tdelta = dt.timedelta(days=-365)
    last_year = format_date + tdelta

    """Getting Temp data for year"""
    results = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date.between(last_year, format_date)).group_by(Measurement.date).all()
    session.close()

    """Preparing data"""
    temp_data = []
    for date, temp in results:
        day_dict={}
        day_dict['date']=date
        day_dict['temp']=temp
        temp_data.append(day_dict)
    
    return jsonify(temp_data)


@app.route("/api/v1.0/<start>")
def startdate(start):
    """Getting temp data starting from start date"""
    session = Session(engine)
    tmin = session.query(Measurement.tobs).filter(Measurement.date>=start).order_by(Measurement.tobs.asc()).first()
    tmax = session.query(Measurement.tobs).filter(Measurement.date>=start).order_by(Measurement.tobs.desc()).first()
    tavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=start).order_by(Measurement.tobs.desc()).all()
    session.close()

    """Formatting data"""
    temp_data = {}
    temp_data['start date']=start
    temp_data['temps']={}
    temp_data['temps']['min']=tmin
    temp_data['temps']['max']=tmax
    temp_data['temps']['avg']=tavg

    return jsonify(temp_data)


@app.route("/api/v1.0/<start>/<end>")
def startenddate(start,end):
    """Getting temp data starting from start date"""
    session = Session(engine)
    tmin = session.query(Measurement.tobs).filter(Measurement.date.between(start,end)).order_by(Measurement.tobs.asc()).first()
    tmax = session.query(Measurement.tobs).filter(Measurement.date.between(start,end)).order_by(Measurement.tobs.desc()).first()
    tavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date.between(start,end)).order_by(Measurement.tobs.desc()).all()
    session.close()

    """Formatting data"""
    temp_data = {}
    temp_data['dates']={}
    temp_data['dates']['start']=start
    temp_data['dates']['end']=end
    temp_data['temps']={}
    temp_data['temps']['min']=tmin
    temp_data['temps']['max']=tmax
    temp_data['temps']['avg']=tavg

    return jsonify(temp_data)



if __name__ == '__main__':
    app.run(debug=True)