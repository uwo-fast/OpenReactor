from sensor import sensor
import time 
import datetime
import struct
from sensor.model.model import Sensor,SensorReading,Control,ControlReading,SensorData

class feedback:
    """
    The init of the class, must take the name of the control system even if it isn't used. 
    """
    def __init__(self,name,I2C):
        self.data=0
        self.params={}
        self.name=name
        self.I2C=I2C

    def getData(self):
        """
        Example of how to read sensor data, this will take the last measurement which should have occured right before the control section was started
        """
        data=SensorReading.select().where(SensorReading.name=='Heater Thermocouple').order_by(SensorReading.time)[-1].value
        self.data=data

    def getParams(self):
        """
        Example of how to expose the current parameters for the control system. 
        If you want to change the parameters use self.I2C.edit_params(newParams) where newParams is the dictionary with the new values. 
        """
        params=ControlReading.select().where(ControlReading.name==self.name).order_by(ControlReading.time)[-1].params
        self.params=params

    def float2byte(self):
        """
        Way of formatting the output float to a byte array that is parsed as a float. 
        """
        self.data=struct.pack('f',self.data)

    def process(self):
        """
        process must have the contain all calls and the return statement. The class is initialised and then process is called. 
        The output is a byte array that will be written to the I2C address defined in devices.json. 
        """
        self.getData()
        self.float2byte()
        self.getParams()
        output=self.data
        return output