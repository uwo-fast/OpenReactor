from tokenize import String
import busio
from .model import model
from .model.model import Sensor,SensorReading
import time
import datetime
import random
import struct
from board import SCL, SDA
from .sensor_format import form

#def form(form,data):
#    """
#    contains the formatting for raw measurements
#    Parameters
#    ----------
#    form : string
#        name of formatting method
#    data : byte array
#        data to be formatted 
#    Returns
#    -------
#    result : string
#        formatted data
#    """
#    result=-1
#    form=form.casefold()
#    print("form:{}".format(form))
#
#    if form=="temp_ada":
#        val=data[0] << 8 | data[1]
#        result=(val & 0xFFF)/16.0
#        if val & 0x1000:
#            result -=256.0
#
#
#    elif form=="atlas":
#        result=list(map(lambda x: chr(x & ~0x80),list(data)))
#        result=result[1:6]
#        result="".join(map(str,result))
#
#    elif form=="byte":
#        result=struct.unpack('f',data)
#        result="".join(map(str,result))
#        
#
#    return result

class I2C:
    """
    Class used to define I2C devices connected to the system, contains methods for measurement and database interfacing
    """
    def __init__(self, name, units,form="atlas", address=99, request_message=0x52, delay=0.9, read_length=31,enabled=-1,params=-1,def_state=False):
        """
        contains all essential information for communication with the device, defaults to atlas pH sensor
        Parameters
        ----------
        name : string
            name of sensor
        units : string
            units of measurement
        form : string
            formatting type
        address : int
            I2C address for sensor
        request_message : int
            I2C register address
        delay : float
            delay in seconds between write and read
        read_length : float
            number of bits to read from register
        """
        self.name = name
        self.units = units
        self.addr = address
        self.req_msg = request_message
        self.delay = delay
        self.read_len = read_length
        self.value = 0.000
        self.time = datetime.datetime.now()
        self.form = form
        self.enabled=enabled
        self.params=params
        self.def_state=def_state
        self.db = model.Data()
        self.def_params=params
        if params==-1:
            self.db.define_sensor(name, units)
        elif params!=-1:
            self.db.define_control(name,units,def_state)


    def __del__(self):
        """Deconstructor to close the connection to the database."""
        self.db.close()


    
    def read(self):
        """Reads from the sensor and places the reading in 'value'."""
        i2c=busio.I2C(SCL, SDA, 400000)
        if type(self.req_msg) is list:
            toWrite=self.req_msg
        else:
            toWrite=[self.req_msg]
        if type(toWrite[0]) is str:
            toWrite[0]=[ord(i) for i in toWrite[0]]
        if len(toWrite) !=0:
            i2c.writeto(self.addr,bytes(toWrite),stop=False)
        result=bytearray(self.read_len)
        time.sleep(self.delay)
        i2c.readfrom_into(self.addr,result)
        result = form(self.form,result)
        #result=list(map(lambda x: chr(x & ~0x80), list(result)))
        #result=result[self.msb_trim:self.lsb_trim]
        #result="".join(map(str,result))
        self.value = result
        self.time = datetime.datetime.now()
        i2c.deinit()

    def write(self):
        """Used for control systems, writes only"""
        i2c=busio.I2C(SCL, SDA, 400000)
        toWrite=self.req_msg
        i2c.writeto(self.addr,bytearray(toWrite),stop=False)
        i2c.deinit()

    def controlMessage(self,message,type='f'):
        """Used to change the byte array that is written to a given address. Store must be called seperately."""
        self.req_msg=message
        #self.value=str(struct.unpack(type,self.req_msg)[0])
        self.time = datetime.datetime.now()
        #print("req_msg :: {}".format(self.req_msg))

    def readFalse(self):
        """Reads a false random float as a measurement :: only use for testing"""
        self.value=random.uniform(4.5,9.5)	
        self.time = datetime.datetime.now()
     
    def readEmpty(self):
        """Reads a value of -1 as a measurement, used for init of sensor to avoid issues"""
        self.value=-1
        self.time = datetime.datetime.now()

    def store(self):
        """Stores the value of the latest sensor reading into the database."""
        if self.params==-1:
            self.db.add_reading(time=self.time, name='{0}'.format(self.name), value=self.value)
        elif self.params!=-1:
            self.db.add_control_status(time=self.time, name='{0}'.format(self.name), value=self.value,enabled=self.enabled,params=self.params)

    def edit_params(self,newParams):
        """Used to edit the params of the control system"""
        self.params=newParams
        self.store()

    def control_state(self,state):
        """Changes the enabled state of the control"""
        self.enabled=state

    def reset_control(self):
        """Resets to default state"""
        print(self.def_state)
        self.enabled=self.def_state
        self.params=self.def_params
        self.store()

    def print_value(self):
        """Prints the most recent sensor value and time of its reading"""
        print("{0}: {1}\n".format(self.time, self.value))

    def print_i2c_info(self):      
        """Prints the sensor's i2c info"""  
        print("Address: {0}\nRead request message: {1}\nRead delay time: {2} seconds\nLength of read: {3} bits\n".format(hex(self.addr), self.req_msg, self.delay, self.read_len))

    def print_db_info(self):
        """Prints the sensor's database info"""
        print("{0} ({1})\n".format(self.name, self.units))

    def print_info(self):
        """Prints all of the sensor's info"""
        self.print_db_info()
        self.print_i2c_info()
        self.print_value()

