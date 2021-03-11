
from kazoo.client import KazooClient
import sys
import time
import random
import json
import zmq


class Broker:

    def __init__(self):
        seld.leader_election() # blocks until/if wins


        with open('config.json','r') as fin:
            config = json.load(fin)
        self.use_broker = config['use_broker']
        self.context = zmq.Context()
        if self.use_broker:
            # Request - Reply socket for publishers
            self.pub_socket = self.context.socket(zmq.REP)
            self.pub_socket.bind("tcp://*:5555")
            # Publish - Subscribe socket for subscribers
            self.port = "5556"
            self.sub_socket = self.context.socket(zmq.PUB)
            self.sub_socket.bind("tcp://*:%s" % self.port)
            # Dictionary for holding subcriber and publisher information
            self.registry = {'PUB':[],'SUB':[]}
        else:
            # This is a proxy. We create the XSUB and XPUB endpoints
            print ("This is proxy: creating xsub and xpubsockets")
            xsubsocket = self.context.socket(zmq.XSUB)
            xsubsocket.bind("tcp://*:5555")
            xpubsocket = self.context.socket (zmq.XPUB)
            xpubsocket.setsockopt(zmq.XPUB_VERBOSE, 1)
            xpubsocket.bind ("tcp://*:5556")
            print('Proxy starting. Blocking...')
            zmq.proxy (xsubsocket, xpubsocket)

    def leader_election():
        zk = KazooClient(hosts='127.0.0.1:2181')
        zk.start()
        data, stat = zk.get("/")
        print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

        election = zk.Election("/electionpath", "actor_1")

        def my_leader_function():
            print('woohoo! I won')
        election.run(my_leader_function)
        # zk.create("/electionpath", ephemeral=False, sequence=False)
        zk.set("/lead_broker/broker1",b"10.0.0.2")

    def run(self):
        with open('config.json','r') as fin:
            config = json.load(fin)
        self.use_broker = config['use_broker']
        if self.use_broker:
            print('run loop')
            while True:
                #  Wait for next request from client
                self.message = self.pub_socket.recv()
                self.decoded_message = self.message.decode("utf-8")
                print('self.decoded_message',self.decoded_message)
                if ',' in self.decoded_message:
                    self.deliminated_message = self.decoded_message.split(',')
                    self.app_type = self.deliminated_message[1]
                    self.ID = self.deliminated_message[2]
                    self.topic = self.deliminated_message[0][:-1]
                    self.message = self.deliminated_message[2]
                    print(self.app_type,self.topic,self.ID,self.message)
                    self.x = set(self.registry[self.app_type])
                    self.x.add(self.ID + ':' + self.topic)
                    self.registry[self.app_type] = self.x
                    print('registry',self.registry)
                    self.messagedata = self.message
                    print("%s %s" % (self.topic, self.messagedata))
                    self.bmessage = str.encode(str(self.topic) + ' ' + str(self.messagedata))
                    self.sub_socket.send(self.bmessage)
                    self.pub_socket.send(b"Published " + self.bmessage)
                else:
                    self.pub_socket.send(b"Published " + self.message)
                time.sleep(.01)
        else:
            pass

def main():
    print('Instantiating the broker')
    broker = Broker()
    broker.run()

#----------------------------------------------
if __name__ == '__main__':
    main ()