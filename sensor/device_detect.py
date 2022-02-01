import os
import busio
import time
import json
from board import *
'''
i2c=busio.I2C(SCL,SDA)
print("Found devices on:",[hex(i) for i in i2c.scan()])
devices = i2c.scan()
for dev in devices:
	print("Device: "+str(dev))
	i2c.writeto(dev,bytes([0x52]),stop=False)
	result=bytearray(31)
	time.sleep(3)
	i2c.readfrom_into(dev,result)
	result=list(map(lambda x: chr(x & ~0x80), list(result)))
	result=result[1:6]
	result="".join(map(str,result))
	print(result)


i2c.deinit()
'''
dir = os.path.abspath(os.getcwd())



class connected:
    def __init__(self,devs=[]):
        #print(dir)
        self.devs=devs
        i2c=busio.I2C(SCL,SDA)
        devices=i2c.scan()
        i2c.deinit()
        for dev in devices:
            addrs=dev
            name=self.find_dev(dev,'name')
            form=self.find_dev(dev,'form')
            unit=self.find_dev(dev,'unit')
            req_msg=self.find_dev(dev,'req_msg')
            delay=self.find_dev(dev,'delay')
            read_length=self.find_dev(dev,'read_length')
            self.devs.append((addrs,name,unit,form,req_msg,delay,read_length))
    def find_dev(self,addr,search):
        file=open(dir+'/devices.json')
        dict=json.load(file)
        for dev in dict['DEVICES']:
            if dev['address']==addr:
                return dev[search]


        