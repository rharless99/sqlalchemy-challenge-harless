from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt
# create engine
engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
# step 1:
app = Flask(__name__)
@app.route("/")
def route_list():
    # urls that tell the user the end points that are available
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def prcp():
   
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    

  
    all_dates = []
    for date, prcp in results:
        all_dates_dict = {}
        all_dates_dict["date"] = date
        all_dates_dict["prcp"] = prcp
       
        all_dates.append(all_dates_dict)

    return jsonify(all_dates)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_results = session.query(Station.name).all()
    session.close()
    stations_list = list(np.ravel(station_results))
    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    LastDay = dt.date(2017, 8, 23)
    OneYearAgo = LastDay - dt.timedelta(days = 365)
    ResultsLastYear = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= OneYearAgo ).filter_by(station ="USC00519281").all()
    session.close()
    tobs_list = list(np.ravel(ResultsLastYear))
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def tobs_start(start):
    session = Session(engine)
    tobs_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    start_dict= []
    for min_temp, avg_temp, max_temp in tobs_start:
        search_date = {}
        search_date['Min Temp'] = min_temp   
        search_date['Avg Temp'] = avg_temp
        search_date['Max Temp'] = max_temp
        start_dict.append(search_date)

    return jsonify(start_dict)

@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end(start, end):
    session = Session(engine)
    t_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()
    session.close()
    t_start_end_dict = []
    for min_temp, avg_temp, max_temp in t_start_end:
        search_date_2 = {}
        search_date_2['Min Temp'] = min_temp   
        search_date_2['Avg Temp'] = avg_temp
        search_date_2['Max Temp'] = max_temp
        t_start_end_dict.append(search_date_2)

    return jsonify(t_start_end_dict)

#2nd step:
if __name__ == '__main__':
    app.run()