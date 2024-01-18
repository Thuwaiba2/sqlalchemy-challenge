from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from datetime import datetime
import numpy as np

app = Flask(__name__)

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to the Climate App API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

# Implement the logic to retrieve precipitation data for the last 12 months
@app.route("/api/v1.0/precipitation")
def precipitation():
    with app.app_context():
        # Calculate the date one year from the last date in data set.
        one_year = datetime.date(2017, 8, 23) - datetime.timedelta(days=365)
        session = Session(engine)
        results = session.query(Measurement.date, Measurement.prcp)\
            .filter(Measurement.date >= one_year).all()
        session.close()

        # Create a dictionary from the row data and append to a list of all_passengers
        precipitation_data = []
        for date, prcp in results:
            measurement_dict = {"date": date, "prcp": prcp}
            precipitation_data.append(measurement_dict)

        # Convert the data to a dictionary and return JSON
        return jsonify(precipitation_data)

# Implement the logic to retrieve station data and return JSON
@app.route("/api/v1.0/stations")
def get_stations():
    with app.app_context():
        # List the stations directly in the query and fetch all results
        session = Session(engine)
        stations = session.query(Station.name).all()
        session.close()

        # Convert the data to a list of dictionaries
        stations_list = [{"name": name} for name, in stations]

        # Convert the data to a dictionary and return JSON
        return jsonify(stations_list)

    # Implement the logic to retrieve temperature observations for the most active station
@app.route("/api/v1.0/tobs")  
def tobs():    
    # Find the most active station
        session = Session(engine)
        most_active_station = session.query(Measurement.station, func.count(Measurement.station))\
            .group_by(Measurement.station)\
            .order_by(func.count(Measurement.station).desc())\
            .first()[0]
        
        # Calculate the date one year from the last date in data set.
        one_year_ago = datetime.date(2017, 8, 23) - datetime.timedelta(days=365)

        # Query temperature observations for the most active station in the previous year
        results = session.query(Measurement.date, Measurement.tobs)\
            .filter(Measurement.station == most_active_station)\
            .filter(Measurement.date >= one_year_ago).all()
        session.close()

        # Create a list of dictionaries
        temperature_observations = [{"date": date, "tobs": tobs} for date, tobs in results]

        # return JSON
        return jsonify(temperature_observations)
        

@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Implement the logic to calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    session = Session(engine)

        # Convert start date string to datetime object
    start_date = datetime.strptime(start, "%Y-%m-%d")

        # Query TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date).all()

    session.close()

        # Create a dictionary with the results
    temperature_stats = list(np.ravel(results))

        # Return the data as JSON
    return jsonify(temperature_stats)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Implement the logic to calculate TMIN, TAVG, and TMAX for dates between start and end (inclusive)
    session = Session(engine)
    try:
        # Convert start and end date strings to datetime objects
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use the format YYYY-MM-DD."}),

    # # Convert start and end date strings to datetime objects
    # start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    # end_date = datetime.datetime.strptime(end, "%Y-%m-%d")

    # Query TMIN, TAVG, and TMAX for the date range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date)\
        .filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary with the results
    temperature_stats = list(np.ravel(results))

    # Return the data as JSON
    return jsonify(temperature_stats)

if __name__ == "__main__":
    app.run(debug=True)