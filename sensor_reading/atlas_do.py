import busio
import time
from board import SCL, SDA

addr = 100
R = 0x52
delay = 0.6 # Time delay needed for the DO sensor

i2c=busio.I2C(SCL, SDA, 400000)
i2c.writeto(addr,bytes([R]),stop=False)
result=bytearray(31)
time.sleep(delay)
i2c.readfrom_into(addr,result)
result=list(map(lambda x: chr(x & ~0x80), list(result)))
result=result[1:6]
result="".join(map(str,result))
print(result)

i2c.deinit()
