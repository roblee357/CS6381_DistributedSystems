"""
=====================================
Discovery Server
=====================================

Used in Brokerless mode- in the discovery phase
- Dictionary holds subscriber and publisher information
"""


import sys
import time
import random
import json
import zmq


class Dserve:

    def __init__(self):
        with open('config.json','r') as fin:
            config = json.load(fin)
        self.port = config['disc_port']
        # Request - Reply socket
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:" + self.port)
        # The publishers do not need to know about the subscribers, but 
        # the subscribers need to know the addresses of the publishers
        # Dictionary for holding subcriber and publisher information
        self.registry = {}
        self.registry['PUB'] = {}
        self.registry['SUB'] = {}

       
    def run(self):
        with open('config.json','r') as fin:
            config = json.load(fin)
        while True:
            #  Wait for next request from client
            print('started loop')
            self.message = self.socket.recv()
            self.decoded_message = self.message.decode("utf-8")
            # print('self.decoded_message',self.decoded_message)
            self.deliminated_message = self.decoded_message.split(',')
            self.app_type = self.deliminated_message[0]
            self.topic = self.deliminated_message[1]
            self.ID = self.deliminated_message[2]
            self.ip = self.deliminated_message[3]
            print(self.app_type,self.topic,self.ID,self.message)
            try:
                self.registry[self.app_type][self.topic][self.ID] = self.ip
            except Exception as e:
                self.registry[self.app_type][self.topic] = { self.ID  :  self.ip }
                print(e)
            ALT = 'SUB' if self.app_type == 'PUB' else 'PUB'
            print(self.registry)
            try:
                reply = json.dumps(self.registry[ALT][self.topic])
            except:
                reply = 'None found'
            self.bmessage = str.encode(ALT + 's discovered: ' + reply)
            self.socket.send(self.bmessage)

def main():
    print('Instantiating the discovery server')
    dserver = Dserve()
    dserver.run()

#----------------------------------------------
if __name__ == '__main__':
    main ()
