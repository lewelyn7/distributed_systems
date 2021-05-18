import random
import time
from enum import Enum 
import pykka


class Status(Enum):
    OK = 1
    BATTERY_LOW = 2
    PROPULSION_ERROR = 3
    NAVIGATION_ERROR = 4


class SatelliteAPI:


    def getStatus(self, satelliteIndex):

        time.sleep((100 + random.randint(0, 400))/1000)
        p = random.random()
        if p < 0.8:
            return Status.OK
        elif p < 0.9:
            return Status.BATTERY_LOW
        elif p < 0.95:
            return Status.NAVIGATION_ERROR
        else:
            return Status.PROPULSION_ERROR


