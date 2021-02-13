
import sys
import time
import random
import json
import zmq
from discovery_server import *

class BorDS:

    def __init__(self):
        with open('config.json','r') as fin:
            self.config = json.load(fin)
        self.use_broker = config['use_broker']
        self.context = zmq.Context()
        if self.use_broker:
            # This is a proxy. We create the XSUB and XPUB endpoints
            print ("This is proxy: creating xsub and xpubsockets")
            xsubsocket = self.context.socket(zmq.XSUB)
            xsubsocket.bind("tcp://*:5555")
            xpubsocket = self.context.socket (zmq.XPUB)
            xpubsocket.setsockopt(zmq.XPUB_VERBOSE, 1)
            xpubsocket.bind ("tcp://*:5556")
            print('Proxy starting. Blocking...')
            zmq.proxy (xsubsocket, xpubsocket)
        else:
            print('Instantiating the discovery server')
            dserver = Dserve()
            dserver.run()

def main():
    print('Instantiating the broker or discovery server')
    bords = BorDS()

#----------------------------------------------
if __name__ == '__main__':
    main ()