import pykka
from RequestActor import RequestActor 
from MonitoringStationActor import SatelliteRequest



class Dispatcher(pykka.ThreadingActor):

    def on_receive(self, msg):
        if isinstance(msg, SatelliteRequest):
            r_actor = RequestActor.start()
            r_actor.tell(msg)

        
