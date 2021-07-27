import busio
import model
import time
import datetime
from board import SCL, SDA


class I2C_Sensor:
    """Used to store all the required information to date from a sensor and store that data to a database"""
    def __init__(self, name, units, address=99, request_message=0x52, delay=0.9, read_length=31, response_most_significant_bit_trim=1, response_least_significant_bit_trim=6):
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

        self.db = model.SensorData()
        self.db.define_sensor(name, units)


    """Deconstructor to close the connection to the database"""
    def __del__(self):
        self.db.close()


    """Reads from the sensor and places the reading in 'value'."""
    def read(self):
        i2c=busio.I2C(SCL, SDA, 400000)
        i2c.writeto(self.addr,bytes([self.req_msg]),stop=False)
        result=bytearray(self.read_len)
        time.sleep(self.delay)
        i2c.readfrom_into(self.addr,result)
        result=list(map(lambda x: chr(x & ~0x80), list(result)))
        result=result[self.msb_trim:self.lsb_trim]
        result="".join(map(str,result))
        self.value = result
        self.time = datetime.datetime.now()
        i2c.deinit()


    """Stores the value of the latest sensor reading into the database"""
    def store(self):
        self.db.add_reading(time=self.time, name='{0}'.format(self.name), value=self.value)

    
