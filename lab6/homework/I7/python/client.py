# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import random
import logging

import grpc

import CryptoEvents_pb2_grpc
import CryptoEvents_pb2



def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    root_cert = open("../cert/rootCA.crt", "rb").read()
    creds = grpc.ssl_channel_credentials(root_cert)

    with grpc.secure_channel('localhost:1443', creds) as channel:
        stub = CryptoEvents_pb2_grpc.CryptoNotifierStub(channel)
        candleRequest = CryptoEvents_pb2.CandleRequest(ticker=CryptoEvents_pb2.t15m, pair="BTC/USDT")
        print(candleRequest)
        candle = stub.getLatestCandle(candleRequest)
        print(candle)



if __name__ == '__main__':
    logging.basicConfig()
    run()