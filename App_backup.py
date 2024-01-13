# Import the dependencies.
from flask import Flask, jsonify; 
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import numpy as np
from datetime import datetime, timedelta


#################################################
# Database Setup
#################################################
# Create an SQLite engine
engine = create_engine("sqlite:///your_hawaii.sqlite")
# Create a session
session = Session(engine)


# Reflect the database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# # Check the tables present in the database 
inspector = inspect(engine)
print(inspector.get_table_names())

session.close()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create a session
session = Session(engine)
#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Welcome to the Climate App API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date (Replace start_date with a valid date format, e.g., 2017-01-01)<br/>"
        f"/api/v1.0/start_date/end_date (Replace start_date and end_date with valid date formats)"
    )


# Implement the logic to retrieve precipitation data for the last 12 months
# Calculate the date one year from the last date in data set.
one_year = datetime.date(2017,8,23)-datetime.timedelta(days=365)
@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= one_year).all()
   
   # Convert the data to a dictionary and return JSON
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Implement the logic to retrieve station data and return JSON
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Implement the logic to retrieve temperature observations for the most active station
    # for the previous year and return JSON
    return jsonify(temperature_data)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Implement the logic to calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    # and return JSON
    return jsonify(temperature_stats)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Implement the logic to calculate TMIN, TAVG, and TMAX for dates between start and end (inclusive)
    # and return JSON
    return jsonify(temperature_data)

if __name__ == "__main__":
    app.run(debug=True)
