from sensor import sensor
import time 
import datetime
import struct
from sensor.model.model import Sensor,SensorReading,Control,ControlReading,SensorData

class feedback:
    def __init__(self,name,I2C):
        self.data=0
        self.dataLast=0
        self.params={}
        self.name=name
        self.I2C=I2C
        self.outputType='f'

    def getData(self):
        #data=SensorReading.select().where(SensorReading.name=='Adafruit Temperature Sensor').order_by(SensorReading.time)[-1].value
        self.getParams
        p=list(self.params)
        del p[-1]
        data=[]
        for i in p:
           data.append(self.params[i])
        self.data=data

    def getParams(self):
        params=ControlReading.select().where(ControlReading.name==self.name).order_by(ControlReading.time)[-1].params
        self.params=params

    def float2byte(self):
        out=b''
        for p in self.data:
           out+=struct.pack(self.outputType,p)
        self.data=out

    def process(self):
        self.getData()
        self.float2byte()
        output=self.data
        return output