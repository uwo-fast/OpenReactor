from sensor.model.model import Sensor, SensorReading
print(Sensor.select())

for dev in Sensor.select():
    print("list:")
    print(dev)
