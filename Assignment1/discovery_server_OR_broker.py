
import sys
import time
import random
import json
import zmq
from discovery_server import *
import argparse, configurator

def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()
    # add optional argument to turn off the broker
    parser.add_argument ("-b","--brokermode",default='broker_on', help="Broker mode. default is broker_on")
    # parse the args
    args = parser.parse_args ()
    return args

class BorDS:

    def __init__(self,args):
        with open('config.json','r') as fin:
            self.config = json.load(fin)
            
        if 'broker_on' in args.brokermode:
            configurator.change('use_broker',True)
            # This is a proxy. We create the XSUB and XPUB endpoints
            print ("This is proxy: creating xsub and xpubsockets")
            self.context = zmq.Context()
            xsubsocket = self.context.socket(zmq.XSUB)
            xsubsocket.bind("tcp://*:5555")
            xpubsocket = self.context.socket (zmq.XPUB)
            xpubsocket.setsockopt(zmq.XPUB_VERBOSE, 1)
            xpubsocket.bind ("tcp://*:5556")
            print('Proxy broker starting. Blocking...')
            zmq.proxy (xsubsocket, xpubsocket)
            sys.stdout.flush()
        else:
            configurator.change('use_broker',False)
            print('Instantiating the discovery server')
            dserver = Dserve()
            sys.stdout.flush()
            dserver.run()

def main():
    args = parseCmdLineArgs ()
    print('Instantiating the broker or discovery server')
    bords = BorDS(args)

#----------------------------------------------
if __name__ == '__main__':
    main ()