import busio
from .model import model
from .model.model import Sensor,SensorReading
import time
import datetime
import random
from board import SCL, SDA

def form(form,data):
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
    """Used to store all the required information to date from a sensor and store that data to a database."""
    def __init__(self, name, units,form="atlas", address=99, request_message=0x52, delay=0.9, read_length=31, response_most_significant_bit_trim=1, response_least_significant_bit_trim=6):
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


    """Deconstructor to close the connection to the database."""
    def __del__(self):
        self.db.close()


    """Reads from the sensor and places the reading in 'value'."""
    def read(self):
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
        self.value=random.uniform(4.5,9.5)	
        self.time = datetime.datetime.now()
    
    def readEmpty(self):
        self.value=-1
        self.time = datetime.datetime.now()

    """Stores the value of the latest sensor reading into the database."""
    def store(self):
        self.db.add_reading(time=self.time, name='{0}'.format(self.name), value=self.value)
    
    """Prints the most recent sensor value and time of its reading"""
    def print_value(self):
        print("{0}: {1}\n".format(self.time, self.value))


    """Prints the sensor's i2c info"""
    def print_i2c_info(self):        
        print("Address: {0}\nRead request message: {1}\nRead delay time: {2} seconds\nLength of read: {3} bits\n{4} most significant bits trimmed off the response\n{5} least significant bits trimmed off the response\n".format(hex(self.addr), self.req_msg, self.delay, self.read_len, self.msb_trim, self.lsb_trim))


    """Prints the sensor's database info"""
    def print_db_info(self):
        print("{0} ({1})\n".format(self.name, self.units))

    
    """Prints all of the sensor's info"""
    def print_info(self):
        self.print_db_info()
        self.print_i2c_info()
        self.print_value()
