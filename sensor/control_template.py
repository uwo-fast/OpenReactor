#Wilson Holmes
#OpenReactor
#Created: 2020/04/16
#Last Modified: 2021/04/16
#Description:
'''This is a template file to be used when adding new sensors to the openreactor.
The website pulls data from both the sensor table and the sensorreading table
in the sqlite3 database to create the graphs. So in order to add a new sensor
you will need to get the data from the sensor, populate the sensor database
with a name and unit for every reading, and put the datetime, sensor name, and
value of the reading in the sensorreading table of the database.
e.g. "Generic-Sensor Temperature" for the name and "°C" for the units in the
sensor table; and "datetime" for the date, "Generic-Sensor Temperature" for the
name, and a numer for the value in the sensorreading table. Look through this
file and its comments to follow how the methods imported from model.py are used
to achieve this. If more reference is needed, SoilSensorReadOnly.py is in this
same directory, and is just this file edited for use with
an adafruit_circuitpython_seesaw sensor. One last thing to note (if you are
still indeed reading this) is that you will need to have a sensor entry for
every value that you wish to store. That is why I formatted the sensor names
like "Generic-Sensor Temperature" as (for many sensors) they can read multiple
values in, so you would need to add another sensor to the database named
"Generic-Sensor [name of other thing being measure e.g. Moisture]" to be able
to properly graph and store the data.'''

import os, sys
p = os.path.abspath('.')
sys.path.insert(1, p)
from model import model
#import model # For saving the sensor data to the database


# Create an instance of our data model access layer object.
# This object takes care of all the Peewee ORM and DB access so our code in this
# file is very simple and just calls function on the model access layer object.
Data = model.SensorData()

# Define which sensors we expect to be connected to the Pi and their units.
control1Name = 'Generic Control Mechanism'
control1Target = 0
control2Name = 'Generic Sensor Moisture'
control2Target= 0

# If there are no prexisting entrys into the sensor table in the databse with
# these exact names and units, then a new entry will be created in the table.
Data.define_control(name = control1Name,target = control1Target)
Data.define_control(name  = control2Name,target = control2Target)
print(model.Control.select().where(model.Control.name==control2Name)[0])

