# Raspberry Pi SQLite Database Sensor Readings pt. 3
# This code creates a basic data model for the project using the Peewee ORM to
# simplfiy access to a SQLite database.  The functionality is exactly the same
# as in pt. 1, but notice how the ORM removes the need to write SQL queries
# embedded in the code.
# Author: Tony DiCola
# License: Public Domain

from peewee import *
from playhouse.sqlite_ext import *
#from playhouse.postgres_ext import *
import json


db = SqliteExtDatabase('../openreactor.db', check_same_thread=False)


# Define data model classes that inherit from the Peewee ORM Model class.
# Each of these classes will be represented by a table in the database that
# Peewee will create and manage.  Each row in the table is an instance of the
# model (like a DHT sensor config, sensor reading, etc).

# User will need to add a sensor for each thing they want to store.
class Sensor(Model):
    name = CharField()
    units = CharField()

    class Meta:
        database = db


class SensorReading(Model):
    time = DateTimeField()
    name = CharField()
    value = FloatField()

    class Meta:
        database = db

class Control(Model):
    name = CharField()
    units=CharField()
    def_state=BooleanField()

    class Meta:
        database = db

class ControlReading(Model):
    time=DateTimeField()
    name=CharField()
    value=FloatField()
    params=JSONField()
    enabled=BooleanField()

    class Meta:
        database = db

class SensorData(object):
    """
    Main data access layer class which provides functions to query DHT sensor
    and sensor reading data from the database.
    """

    def __init__(self):
        """Initialize access to the DHT sensor reading database."""
        db.connect(reuse_if_open=True)
        db.create_tables([Sensor, SensorReading,Control,ControlReading], safe=True)

    def define_sensor(self, name, units):
        """Define the specified sensor and add it to the database.  If a sensor
        of the same name, type, and pin exists then nothing will be added.
        """
        Sensor.get_or_create(name=name, units=units)

    def define_control(self,name,units,def_state):
        """Define the specified control and add it to the database.  If a control
        of the same name, type, and pin exists then nothing will be added.
        """
        Control.get_or_create(name=name,units=units,def_state=def_state)

    def get_control(self):
        """Returns a list of all the controls defined in the database."""
        return Control.select()

    def get_sensors(self):
        """Return a list of all the sensors defined in the database.
        Each instace in the list is a Sensor object.
        """
        return Sensor.select()

    def add_control_status(self,time,name,value,params,enabled):
        """Add a new status to the ControlReading table
        """
        ControlReading.create(time=time,name=name,value=value,params=params,enabled=enabled)
    def get_recent_readings(self, name, limit=30):
        """Return a list of the most recent sensor readings with the specified
        name.  By default returns the last 30 readings in descending time order,
        but you can request a different number with the limit parameter.
        """
        return SensorReading.select() \
                            .where(SensorReading.name == name) \
                            .order_by(SensorReading.time.desc()) \
                            .limit(limit)

    def add_reading(self, time, name, value):
        """Add the specified sensor reading to the database."""
        SensorReading.create(time=time, name=name, value=value)

    def close(self):
        """Close the connection to the database."""
        db.close()
