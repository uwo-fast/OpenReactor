from sensor import sensor
import time 
import datetime
import struct
from sensor.model.model import Sensor,SensorReading,Control,ControlReading,Data
from control.PID import PID

class feedback:
    def __init__(self,name,I2C):
        self.data=0
        self.dataLast=0
        self.params={}
        self.name=name
        self.I2C=I2C
        self.identifier=72
        self.outputType='b'

    def getData(self):
        #data=SensorReading.select().where(SensorReading.name=='Adafruit Temperature Sensor').order_by(SensorReading.time)[-1].value
        self.getParams
        p=list(self.params)
        del p[-1]
        self.params["input"]=SensorReading.select().where(SensorReading.name=="Slice 1 :: Temp 1").order_by(SensorReading.id.desc()).get().value
        self.params["lastInput"]=SensorReading.select().where(SensorReading.name=="Slice 1 :: Temp 1").order_by(SensorReading.id.desc()).limit(2)[-1].value
        data,self.params["er"]=PID(self.params["input"],self.params["lastInput"],self.params["setpoint"],self.params["kp"],self.params["ki"].self.params["kd"],er=self.params["er"])
        self.data=data

    def getParams(self):
        params=ControlReading.select().where(ControlReading.name==self.name).order_by(ControlReading.time)[-1].params
        self.params=params

    def params2data(self):
      id=struct.pack(self.outputType,self.identifier)
      p=struct.pack(self.outputType,int(self.data)) 
      self.data=id+p

    def process(self):
        self.getData()
        self.params2data()
        self.I2C.edit_params(self.params)
        output=self.data
        return output
    def reset(self):
        default=ControlReading.select().where(ControlReading.name==self.name).order_by(ControlReading.time.asc()).get().params
        id=struct.pack(self.outputType,self.identifier)
        p=struct.pack(self.outputType,int(0))
        return (id+p)