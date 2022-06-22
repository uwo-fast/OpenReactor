from sensor import sensor
import time 
import datetime
import struct
from sensor.model.model import Sensor,SensorReading,Control,ControlReading,SensorData
"""
An example of a feedback mechanism. 
REQUIRED
--------
Class must be named feedback
Must take the name of the control as an init argument
Must return a packed float that is the commmand to send over I2C to the device specified in 'devices.json' 
Return must be from a function called process that does not take any required arguments. 
Must have property self.outputType which is a string defining what the byte is packed as, ie. 'f'

'devices.json' DEVICE LAYOUT
---------------------
The following is an example for the DEVICE section of devices.json it contains the definition of three different control mechanisms. 
NOTE: in the first section two mechanisms are defined that will write to the same I2C address (in this case 97). This must be done in this manner and they cannot be listed seperately as you would for devices with seperate addresses.
name: The string that is used as a name for the control
address : The I2C address for the output, that means if you wanted to send a command to the pump board for example, you used the pump board address. 
unit : The unit of the measurement, can just be empty string
req_msg : The initial request message to be sent to I2C device, this is what is overwritten in this program so this is just an init
delay : the delay between read and write for sensors, this is not actually used for controls but is still required for parse 
read_length : length of bytes to read, not actually used for controls but is still required for parse
enabled : this is legacy but I'm too lazy right now to fix it, these values are overwritten so don't really matter, must be binary 
params : a sub-dictionary of custom parameters for each control system. NOTE that the only required parameter is '"control": model.demo' where model.demo is the absolute path to the feedback mechanism .py file. (model.demo is equivalent to model/demo.py) 
         parameters must be a single integer to be parsed by interface at the moment but can have any number of parameters.  
def_state : the default state of the control systems, on : true, off : false

"CONTROLS":[
   {
      "name":["Control Test","Control Test 2"],
      "address":97,
      "unit":["",""],
      "form":["byte","byte"],
      "req_msg":[[82,72],54],
      "delay":[0.0,0.0],
      "read_length":[4,4],
      "enabled":[true,false],
      "params":[{
         "min":0,
         "max":0,
         "control":"control.demo"
      },
      {
         "min":0,
         "max":0,
         "control":"control.demo"
      }
   ],
      "def_state":[true,false]
   },
   {
      "name":"Control Test 3",
      "address":96,
      "unit":"",
      "form":"byte",
      "req_msg":[82,72],
      "delay":0.0,
      "read_length":4,
      "enabled":false,
      "params":{
         "min":0,
         "max":0,
         "target":100,
         "control":"control.demo"
      },
      "def_state":true
   }
]

"""

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
        self.outputType='f'

    def getData(self):
        """
        Example of how to read sensor data, this will take the last measurement which should have occured right before the control section was started
        """
        data=SensorReading.select().where(SensorReading.name=='Adafruit Temperature Sensor').order_by(SensorReading.time)[-1].value
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
        self.data=struct.pack(self.outputType,self.data)

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