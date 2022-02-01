import sensor
from model.model import Sensor,SensorReading

def form(form,data):
    result=-1
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