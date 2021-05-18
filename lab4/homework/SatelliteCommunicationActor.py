import pykka
from SatelliteAPI import SatelliteAPI, Status
import time

class ApiQuery:
    who = 0
    sat_id = 0
    timeout = 0

class ApiResponse:
    sat_id = 0
    timer = 0
    status = None



class SatelliteCommunicationActor(pykka.ThreadingActor):
    def __init__(self):
        super().__init__()
        self.sat = SatelliteAPI()

    def on_receive(self, msg):
        if isinstance(msg, ApiQuery):
            r_msg = ApiResponse()
            r_msg.sat_id = msg.sat_id

            start = time.time()
            r_msg.status = self.sat.getStatus(msg.sat_id)
            stop = time.time()
            r_msg.timer = (stop - start)*1000
            response_to = pykka.ActorRegistry.get_by_urn(msg.who)
            if response_to:
                response_to.tell(r_msg)
            self.stop()

        else:
            raise TypeError