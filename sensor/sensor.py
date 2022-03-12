import busio
from .model import model
from .model.model import Sensor,SensorReading
import time
import datetime
import random
from board import SCL, SDA

def form(form,data):
    """
    contains the formatting for raw measurements
    Parameters
    ----------
    form : string
        name of formatting method
    data : byte array
        data to be formatted 
    Returns
    -------
    result : string
        formatted data
    """
    result=-1
    form=form.casefold()
    print("form:{}".format(form))

    if form=="temp_ada":
        val=data[0] << 8 | data[1]
        result=(val & 0xFFF)/16.0
        if val & 0x1000:
            result -=256.0


    elif form=="atlas":
        result=list(map(lambda x: chr(x & ~0x80),list(data)))
        result=result[1:6]
        result="".join(map(str,result))

    return result

class I2C:
    """
    Class used to define I2C devices connected to the system, contains methods for measurement and database interfacing
    """
    def __init__(self, name, units,form="atlas", address=99, request_message=0x52, delay=0.9, read_length=31, response_most_significant_bit_trim=1, response_least_significant_bit_trim=6):
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
        response_most_significant_bit_trim : int
            number of bits to trim from MSB
        response_least_significant_bit_trim : int
            number of bits to trim from LSB
        """
        self.name = name
        self.units = units
        self.addr = address
        self.req_msg = request_message
        self.delay = delay
        self.read_len = read_length
        self.msb_trim = response_most_significant_bit_trim
        self.lsb_trim = response_least_significant_bit_trim
        self.value = 0.000
        self.time = datetime.datetime.now()
        self.form = form
        self.db = model.SensorData()
        self.db.define_sensor(name, units)


    def __del__(self):
        """Deconstructor to close the connection to the database."""
        self.db.close()


    
    def read(self):
        """Reads from the sensor and places the reading in 'value'."""
        i2c=busio.I2C(SCL, SDA, 400000)
        i2c.writeto(self.addr,bytes([self.req_msg]),stop=False)
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
        self.db.add_reading(time=self.time, name='{0}'.format(self.name), value=self.value)
    
    def print_value(self):
        """Prints the most recent sensor value and time of its reading"""
        print("{0}: {1}\n".format(self.time, self.value))

    def print_i2c_info(self):      
        """Prints the sensor's i2c info"""  
        print("Address: {0}\nRead request message: {1}\nRead delay time: {2} seconds\nLength of read: {3} bits\n{4} most significant bits trimmed off the response\n{5} least significant bits trimmed off the response\n".format(hex(self.addr), self.req_msg, self.delay, self.read_len, self.msb_trim, self.lsb_trim))

    def print_db_info(self):
        """Prints the sensor's database info"""
        print("{0} ({1})\n".format(self.name, self.units))

    def print_info(self):
        """Prints all of the sensor's info"""
        self.print_db_info()
        self.print_i2c_info()
        self.print_value()
