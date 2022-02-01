from sensor import sensor
from sensor.model.model import Sensor,SensorReading

#do = sensor.I2C(name="Dissolved Oxygen", units="% Oxygen", address=100, delay=0.6)
ph = sensor.I2C(name="pH", units="pH")
#do.read()
#do.readFalse()
#do.store()
ph.read()
#ph.readFalse()
ph.store()

#do.print_info()
ph.print_info()

for Time in SensorReading.select():
	print(Time.time)
#del do
del ph
