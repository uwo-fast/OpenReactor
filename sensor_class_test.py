import sensor

ph = sensor.I2C(name="pH", units="pH")

ph.read()
ph.print_info()
ph.store()
