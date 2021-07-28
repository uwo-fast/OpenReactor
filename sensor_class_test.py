import sensor

do = sensor.I2C(name="Dissolved Oxygen", units="% Oxygen", address=100, delay=0.6)
ph = sensor.I2C(name="pH", units="pH")

do.read()
do.store()
ph.read()
ph.store()

do.print_info()
ph.print_info()

del do
del ph
