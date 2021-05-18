import pykka
import logging
from collections import Counter
import time
from DBActor import DBActor, DBUpdateRequest, DBStatRequest, DBStatResponse

class SatelliteRequest:
    query_id = 0
    first_sat_id = 0
    id_range = 0
    timeout = 0
    who = 0

class SatelliteAnswer:
    query_id = 0
    data = {}
    time_success_rate = 0


class TestCaseMsg:
    messages = []
    time_interval = 0

class TestCaseMsg2:
    pass

class MonitoringStationActor(pykka.ThreadingActor):
    def __init__(self, name, dispatcher, db_actor):
        super().__init__()
        self.name = name
        self.req_cnt = 0
        self.dispatcher = dispatcher
        self.logger = logging.getLogger(self.__class__.__name__)
        self.timestamps = {}
        self.db_actor = db_actor

    def on_receive(self, msg):
        if isinstance(msg, TestCaseMsg):
            self.logger.debug("got testcase msg")
            for m in msg.messages:
                req = SatelliteRequest()
                req.who = self.actor_urn
                req.query_id = self.req_cnt
                req.timeout = m['timeout']
                req.first_sat_id = m['first_sat_id']
                req.id_range = m['range']
                self.timestamps[self.req_cnt] = time.time()
                self.dispatcher.tell(req)
                self.req_cnt += 1
                
        elif isinstance(msg, SatelliteAnswer):
            stop_time = time.time()
            output = [self.name]
            output.append(f"time: {(stop_time - self.timestamps[msg.query_id])*1000}")
            output.append(f"q_id: {msg.query_id} success_rate: {msg.time_success_rate}")
            output.append(f"errors: {len(msg.data)}")
            # errors_rate = Counter([msg.data[k] for k in msg.data.keys()])
            # for e in errors_rate:
            #     output.append(f"{e} : {errors_rate[e]}")
            for e in msg.data.keys():
                output.append(f"{e} {msg.data[e]}")
            output.append("\r\n")
            print("\r\n".join(output))
            db_msg = DBUpdateRequest()
            db_msg.sats_errors = [(s, 1) for s in msg.data.keys()]
            self.db_actor.tell(db_msg)
        elif isinstance(msg, TestCaseMsg2):
            with_errors_cnt = 0
            for i in range(100, 200):
                q_msg = DBStatRequest()
                q_msg.sat_id = i
                sat_stat = self.db_actor.ask(q_msg, block=True)
                if sat_stat.error_cnt > 0:
                    with_errors_cnt +=1
                    print(f"{sat_stat.sat_id} {sat_stat.error_cnt}")
            print(f"{with_errors_cnt} satellites returned at least one error")
        else:
            raise TypeError
            # start Tests
        
