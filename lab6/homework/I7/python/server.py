import yaml
import CryptoEvents_pb2_grpc
import CryptoEvents_pb2
import grpc
import logging
from concurrent import futures
import threading
import time
import sys

import queue
import random


class PriceCandle:
    def __init__(self):
        self.price_open = random.random()
        self.price_high = random.random()
        self.price_low = random.random()
        self.price_close = random.random()


class CryptoNotifierServicer(CryptoEvents_pb2_grpc.CryptoNotifierServicer):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger().getChild(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.request_cnt = 1
    def getLatestCandle(self, request, context):
        self.logger.debug(f"request_cnt: {self.request_cnt}")
        self.logger.debug(request)
        self.request_cnt+=1
        price = PriceCandle()
        return CryptoEvents_pb2.CandleResponse(open=price.price_open,
                                               high=price.price_high,
                                               low=price.price_low,
                                               close=price.price_close)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    CryptoEvents_pb2_grpc.add_CryptoNotifierServicer_to_server(
        CryptoNotifierServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def serve2():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    CryptoEvents_pb2_grpc.add_CryptoNotifierServicer_to_server(
        CryptoNotifierServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if sys.argv[1] == "1":
        serve()
    else:
        serve2()