import Ice
import sys
import logging
import Office
import datetime
import time
from enum import Enum
import queue
import random
import threading

class CaseTypes(Enum):
    DRIVING_LICENSE = 1
    ZUS_INFO = 2
    BUILDING_PERMIT = 3

class OfficeWorker(threading.Thread):
    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger().getChild(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        self.listeners = {}
        self.cases = []
        self.casesIDcounter = 0
    
    def add_case(self, case):
        case.id = self.casesIDcounter
        self.cases.append(case)
        self.casesIDcounter+=1
        self.logger.info(f"registered case {case.case_type} id:{case.id}; estimated time to resolve: {int(case.endTime-case.startTime)} s")
        return self.casesIDcounter-1

    def register_listener(self, who, listener):
        self.logger.info(f"registered listener for {who}")
        self.listeners[who] = {'proxy': listener, 'attempt_cnt': 0}
    def run(self):
        done = []
        while True:
            self.logger.debug("Worker heart beat")
            for case in self.cases:
                if case.endTime <= time.time():
                    try:
                        self.logger.info(f"case {case.id} is done; sending notify to {case.who}")
                        self.listeners[case.who]['proxy'].notify(Office.Result(True, case.id, case.endTime - case.startTime))
                        done.append(case)
                    except (Ice.Exception, KeyError):
                        self.logger.warning(f"couldnt notify {case.who}, client disconnected")
            for case in done:
                self.cases.remove(case)
            done.clear()
            time.sleep(1)



class OfficeCase:
    def __init__(self, who, case_type, params):
        self.who = who
        self.case_type = case_type
        self.params = params
        self.id = None
        self.startTime = time.time() # TODO get timestamp
        self.endTime = time.time() + random.randint(3,10)



class OfficeProviderI(Office.OfficeProvider):

    def __init__(self):
        super().__init__()
        
        self.cases = {}
        self.casesIDs = 0
        self.officeWorker = OfficeWorker()
        self.officeWorker.start()

    def _add_case(self, case):
        return self.officeWorker.add_case(case)

    def getDrivingLicense(self, who, driving_type, exam, context):
        logging.debug(f"get driving license {who} {driving_type} {exam}")
        return self._add_case(OfficeCase(who, CaseTypes.DRIVING_LICENSE, {'exam': exam, 'driving_type': driving_type}))

    def getZUSInfo(self, who, nip, context):
        logging.debug(f"zus info {who} {nip}")
        return self._add_case(OfficeCase(who, CaseTypes.ZUS_INFO, {'nip': nip}))

    def getBuildingPermit(self, who, where, size):
        logging.debug(f"building permit {who} {where} {size}")
        return self._add_case(OfficeCase(who, CaseTypes.BUILDING_PERMIT, {'where': where, 'size': size}))


    def listen(self, who, listener, current):
        logging.debug(f"listen {who}")
        self.officeWorker.register_listener(who, listener.ice_fixed(current.con))



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with Ice.initialize(['--Ice.ThreadPool.Client.Size=2', '--Ice.ThreadPool.Server.Size=2']) as communicator:
        adapter = communicator.createObjectAdapterWithEndpoints("SimpleOfficeAdapter", "default -p 10000")
        OfficeObject = OfficeProviderI()
        adapter.add(OfficeObject, communicator.stringToIdentity("SimpleOfficeAdapter"))
        adapter.activate()
        logging.info("listen for clients...")
        communicator.waitForShutdown()
        communicator.destroy()