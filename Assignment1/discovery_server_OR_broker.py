
import sys
import time
import random
import json
import zmq
from discovery_server import *
import argparse, configurator
from kazoo.client import KazooClient
import getIP

def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()
    # add optional argument to turn off the broker
    parser.add_argument ("-b","--brokermode",default='broker_on', help="Broker mode. default is broker_on")
    # parse the args
    # add positional arguments in that order
    parser.add_argument ("id", help="ID")
    args = parser.parse_args ()
    return args

class BorDS:

    def __init__(self,args):
        self.args = args
        self.IP = getIP.get()
        with open('config.json','r') as fin:
            self.config = json.load(fin)
        self.leader_election() # blocks until/if wins
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

    def leader_election(self):
        zk = KazooClient(hosts=self.config['zkip']+':2181')
        zk.start()
        data, stat = zk.get("/")
        print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
        election = zk.Election("/electionpath", "broker_" + str(self.args.id))
        election.run(self.my_leader_function)
        # zk.create("/electionpath", ephemeral=False, sequence=False)
        try:
            zk.delete("/lead_broker",recursive=True)
        except:
            print("no leader zNode")
        zk.ensure_path("/lead_broker/broker" + str(self.args.id))
        zk.set("/lead_broker/broker" + str(self.args.id),bytes(self.IP,'utf-8'))

    def my_leader_function(self):
        print('woohoo! I won')

def main():
    args = parseCmdLineArgs ()
    print('Instantiating the broker or discovery server')
    bords = BorDS(args)

#----------------------------------------------
if __name__ == '__main__':
    main ()