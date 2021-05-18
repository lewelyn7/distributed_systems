from MonitoringStationActor import MonitoringStationActor
from MonitoringStationActor import TestCaseMsg, TestCaseMsg2
from Dispatcher import Dispatcher
from DBActor import DBActor
import time
import random
import logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    dispatcher = Dispatcher.start()
    db_actor = DBActor.start()
    stations = []
    stations.append(MonitoringStationActor.start("station1", dispatcher, db_actor))
    stations.append(MonitoringStationActor.start("station2", dispatcher, db_actor))
    stations.append(MonitoringStationActor.start("station3", dispatcher, db_actor))

    for i in range(3):
        msg = TestCaseMsg()
        msg.time_interval = 1
        msg.messages = [
            {
                "first_sat_id": 100 + random.randint(0,50),
                "range": 50,
                "timeout": 300
            },
            {
                "first_sat_id": 100 + random.randint(0,50),
                "range": 50,
                "timeout": 300
            }
        ]

        stations[i].tell(msg)
    
    time.sleep(1)
    stations[0].tell(TestCaseMsg2())


    # time.sleep(120)
