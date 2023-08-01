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
    def __init__(self):
        #print(dir)
        self.devs=[]
        self.cons=[]
        i2c=busio.I2C(SCL,SDA)
        devices=i2c.scan()
        i2c.deinit()
        file=open(dir+'/devices.json')
        full_dict=json.load(file)
        dev_dict=full_dict["DEVICES"]
        con_dict=full_dict["CONTROLS"]
        self.dev=dev_dict
        self.con=con_dict
        for dev in devices:
            addrs=dev
            dev_name=self.find_dev(dev,'name')
            con_name=self.find_con(dev,'name')
            #print(con_name)
            if dev_name:
                form=self.find_dev(dev,'form')
                unit=self.find_dev(dev,'unit')
                req_msg=self.find_dev(dev,'req_msg')
                delay=self.find_dev(dev,'delay')
                read_length=self.find_dev(dev,'read_length')
                if type(dev_name) is list:
                    for i in range(len(dev_name)):
                        try:
                            self.devs.append((addrs,dev_name[i],unit[i],form[i],req_msg[i],delay[i],read_length[i]))
                        except:
                            raise Exception("\nIssue assigning device information for addresses with more than one device.\n Ensure that in devices.json all arguments except for address are arrays of the same length.") 
                else:
                    self.devs.append((addrs,dev_name,unit,form,req_msg,delay,read_length))
            if con_name:
                #print("In Loop")
                form=self.find_con(dev,'form')
                unit=self.find_con(dev,'unit')
                req_msg=self.find_con(dev,'req_msg')
                delay=self.find_con(dev,'delay')
                read_length=self.find_con(dev,'read_length')
                enabled=self.find_con(dev,'enabled')
                params=self.find_con(dev,'params')
                def_state=self.find_con(dev,'def_state')
                if type(con_name) is list:
                    for i in range(len(con_name)):
                        try:
                            self.cons.append((addrs,con_name[i],unit[i],form[i],req_msg[i],delay[i],read_length[i],enabled[i],params[i],def_state[i]))
                        except:
                            raise Exception("\nIssue assigning device information for addresses with more than one device.\n Ensure that in devices.json all arguments except for address are arrays of the same length.")
                else:
                    self.cons.append((addrs,con_name,unit,form,req_msg,delay,read_length,enabled,params,def_state))
            elif not con_name and not dev_name:
                print("Unknown Device found with addr :: {}".format(addrs))

    def find_dev(self,addr,search):
        for dev in self.dev:
            if dev['address']==addr:
                return dev[search]
    def find_con(self,addr,search):
        for con in self.con:
            if con['address']==addr:
                return con[search]

        
