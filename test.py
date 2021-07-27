import busio
import time
from board import *
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
