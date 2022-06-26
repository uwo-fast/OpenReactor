from sensor import sensor
import time 
import datetime
import struct
from sensor.model.model import Sensor,SensorReading,Control,ControlReading,SensorData

#the motor ID, just used as first byte

class feedback:
    """
    The init of the class, must take the name of the control system even if it isn't used. 
    """
    def __init__(self,name,I2C):
        self.data=0
        self.dataLast=0
        self.params={}
        self.name=name
        self.I2C=I2C
        self.motorID=1
        self.outputType='b'

    def getParams(self):
        """
        Example of how to expose the current parameters for the control system. 
        If you want to change the parameters use self.I2C.edit_params(newParams) where newParams is the dictionary with the new values. 
        """
        params=ControlReading.select().where(ControlReading.name==self.name).order_by(ControlReading.time)[-1].params
        self.params=params

    def params2data(self):
      id=struct.pack(self.outputType,self.motorID)
      p=struct.pack(self.outputType,int(self.params["speed"])) #assuming that param is called speed
      self.data=id+p


    def process(self):
        """
        process must have the contain all calls and the return statement. The class is initialised and then process is called. 
        The output is a byte array that will be written to the I2C address defined in devices.json. 
        """
        self.getParams()
        self.params2data()

        output=self.data
        return output

    def reset(self):
        default=ControlReading.select().where(ControlReading.name==self.name).order_by(ControlReading.time.asc()).get().params
        id=struct.pack(self.outputType,self.motorID)
        p=struct.pack(self.outputType,int(default["speed"]))
        return (id+p)