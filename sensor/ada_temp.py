import busio
from board import SCL,SDA

def form(form,data):
    result= -1
    if form=="temp_ada":
        val = data[0] << 8 | data[1] 
        result = (val & 0xFFF) /16.0
        if val & 0x1000:
            result -=256.0
    return result

i2c=busio.I2C(SCL,SDA,400000)
i2c.writeto(25, bytes([5]),stop=False)
result=bytearray(2)
i2c.readfrom_into(25, result)
result=form("temp_ada",result)

print(result)
i2c.deinit()

