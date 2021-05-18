import pykka

from MonitoringStationActor import SatelliteRequest, SatelliteAnswer
from SatelliteCommunicationActor import SatelliteCommunicationActor, ApiQuery, ApiResponse
from SatelliteAPI import Status
import logging
import time
class RequestActor(pykka.ThreadingActor):

    class OverMessage:
        pass

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.results = []
        # self.logger.setLevel(logging.DEBUG)

    def collect_data(self):
        results = self.results
        msg = self.request

        response_to = pykka.ActorRegistry.get_by_urn(msg.who)
        monitoring_ans = SatelliteAnswer()
        monitoring_ans.query_id = msg.query_id
        monitoring_ans.data = {}
        for r in results:

            if r.status != Status.OK:
                monitoring_ans.data[r.sat_id] = r.status

        self.logger.debug([r.timer for r in results])
        self.logger.debug(len(results))
        monitoring_ans.time_success_rate = (len(results))/msg.id_range
        response_to.tell(monitoring_ans)

        self.stop()

    def on_receive(self, msg):

        if isinstance(msg, SatelliteRequest):
            self.request = msg
            self.logger.debug(f" msg.who: {msg.who}")

            self.actors = []
            futures = []
            for sat in range(msg.first_sat_id, msg.first_sat_id + msg.id_range):
                api_actor = SatelliteCommunicationActor.start()
                self.actors.append(api_actor)
                api_query = ApiQuery()
                api_query.sat_id = sat
                api_query.who = self.actor_urn
                api_query.timeout = msg.timeout
                futures.append(api_actor.ask(api_query, block=False))
            self.produce_timeout()

        elif isinstance(msg, ApiResponse):
            self.logger.debug(f"response { msg.sat_id } {msg.status}")
            self.results.append(msg)
            if len(self.results) == self.request.id_range:
                self.collect_data()
        elif isinstance(msg, self.OverMessage):
            self.collect_data()
                    
        else:
            raise TypeError
    
    def produce_timeout(self):
        time.sleep(self.request.timeout / 1000)
        self.actor_ref.tell(self.OverMessage())