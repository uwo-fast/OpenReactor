from sensor import sensor
import time 
import datetime
from sensor.model.model import Sensor,SensorReading,Control,ControlReading,SensorData


class feedback:
    def __init__(self,name):
        self.data=0
        self.dataLast=0
        self.params={}
        self.name=name

    def getData(self):
        data=SensorReading.select().where(SensorReading.name=='Adafruit Temperature Sensor').order_by(SensorReading.time)[-1].value
        self.data=data

    def getParams(self):
        params=ControlReading.select().where(ControlReading.name==self.name).order_by(ControlReading.time)[-1].params
        self.params=params

    def float2byte(self):
        dataString=str(self.data)
        self.data=dataString.encode()


    def process(self):
        self.getData()
        self.float2byte()
        output=self.data
        return output