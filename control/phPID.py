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
        self.identifier=1
        self.outputType='b'
        self.baseID=1
        self.acidID=2
        
        

    def resetPumps(self):
        id=struct.pack(self.outputType,self.baseID)
        p=struct.pack(self.outputType,0)
        self.I2C.controlMessage(id+p)
        self.I2C.write()
        id=struct.pack(self.outputType,self.acidID)
        self.I2C.controlMessage(id+p)
        self.I2C.write()

    def getData(self):
        #data=SensorReading.select().where(SensorReading.name=='Adafruit Temperature Sensor').order_by(SensorReading.time)[-1].value
        self.getParams()
        p=list(self.params)
        print("Params :: {}".format(p))
        del p[-1]
        self.params["input"]=SensorReading.select().where(SensorReading.name=="pH").order_by(SensorReading.id.desc()).get().value
        self.params["lastInput"]=SensorReading.select().where(SensorReading.name=="pH").order_by(SensorReading.id.desc()).limit(2)[-1].value
        data,self.params["er"]=PID(float(self.params["input"]),float(self.params["lastInput"]),float(self.params["setpoint"]),float(self.params["kp"]),float(self.params["ki"]),float(self.params["kd"]),er=float(self.params["er"]),min=-100)
        self.data=abs(data)

    def getParams(self):
        params=ControlReading.select().where(ControlReading.name==self.name).order_by(ControlReading.time)[-1].params
        self.params=params

    def params2data(self):
      if float(self.params["input"])-float(self.params["setpoint"])<0: #if the solution is below target pH, want to add base so use output byte for base pump
        self.identifier=self.baseID
        self.params['Acid Pump']=0
        self.params['Base Pump']=self.data
      else: #if the solution is above or at target pH, want to add acid so use output byte for acid pump
        self.identifier=self.acidID
        self.params['Acid Pump']=self.data
        self.params['Base Pump']=0
      id=struct.pack(self.outputType,self.identifier)
      p=struct.pack(self.outputType,int(self.data)) 
      self.data=id+p

    def process(self):
        self.getData()
        self.resetPumps()
        self.params2data()
        self.I2C.edit_params(self.params)
        output=self.data
        return output
    def reset(self):
        self.resetPumps()
        default=ControlReading.select().where(ControlReading.name==self.name).order_by(ControlReading.time.asc()).get().params
        id=struct.pack(self.outputType,self.identifier)
        p=struct.pack(self.outputType,int(0))
        return (id+p)
