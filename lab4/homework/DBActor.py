import pykka
from tinydb import TinyDB, Query


class DBUpdateRequest:
    sats_errors = []

class DBStatRequest:
    sat_id = 0

class DBStatResponse:
    sat_id = 0
    error_cnt = 0



class DBActor(pykka.ThreadingActor):
    
    def __init__(self):
        super().__init__()
        self.db = TinyDB('db.json')
        self.db.truncate()
        for i in range(100, 200):
            self.db.insert({
                "sat_id": i,
                "error_cnt": 0
            })

    def on_receive(self, msg):
        if isinstance(msg, DBUpdateRequest):            
            sat_query = Query()
            for r in msg.sats_errors:
                sat = self.db.search(sat_query.sat_id == r[0])[0]
                self.db.update({"error_cnt": sat['error_cnt']+r[1]}, sat_query.sat_id == r[0])
        elif isinstance(msg, DBStatRequest):
            sat_query = Query()
            sat = self.db.search(sat_query.sat_id == msg.sat_id)[0]
            response = DBStatResponse()
            response.sat_id = sat['sat_id']
            response.error_cnt = sat['error_cnt']
            return response

        else:
            raise TypeError