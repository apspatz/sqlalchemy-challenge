import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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


"""
@app.route("/api/v1.0/<start>")


""""""
@app.route("/api/v1.0/<start>/<end>")
"""



if __name__ == '__main__':
    app.run(debug=True)