from datetime import datetime
import json
import time
import os
import multiprocessing
from sensor import sensor
from sensor.model.model import Sensor, SensorReading, Control, SensorData
from sensor.device_detect import connected as ct
from experiments.experiments import experiment


class experimentCycle(object):
    def __init__(self, state=False, interval=30):
        self.cores = multiprocessing.cpu_count()
        self.state = state
        self.interval = interval
        print("Number of Cores :: {}".format(self.cores))

    def test(self, time):
        multiprocessing.Lock().acquire()
        p = multiprocessing.Pool(1)
        for i in time:
            p.apply(self.time, [i])
        p.close()
        p.join()

    def time(self, interval):
        if self.state:
            print("Starting Cycle :: {} Seconds".format(interval))
            time.sleep(interval)
            print("Finished Cycle")


# a = experimentCycle(True)
# a.test([1,2,3])
