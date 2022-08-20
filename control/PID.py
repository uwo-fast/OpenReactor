from sensor import sensor
import time 
import datetime
import struct
from sensor.model.model import Sensor,SensorReading,Control,ControlReading,SensorData

def PID(input,lastInput,setpoint,kp,ki,kd,er=0):
    e=setpoint-input
    er+=e
    ei=input-lastInput
    out=kp*e+ki*er-kd*ei
    if out>100:out=100
    if out<0:out=0
    return out,er

