#
#   CS6381 Distributed Systems
#   Spring 2021
#   Assignment 1
#   Team 5 "El Sinko"
#   Rob Lee (robert.e.lee.1@vanderbilt.edu) and Jess Phelan (Jessica.phelan@vanderbilt.edu)
#   Publisher API
#

from discovery_client import *
import zmq,  json, sys
import argparse, time
from datetime import datetime
import configurator
from kazoo.client import KazooClient
import getIP
import watchers
import random

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)
print('hello now')

def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()
    # add optional arguments
    parser.add_argument ("-o", "--ownership", default=str(round(random.uniform(0, 1),3)),help="Ownership. Default: random.uniform(0,1)")
    parser.add_argument ("-his", "--history",  default=10, help="Ownership. Default: random.uniform(0,1)")



    # parser.add_argument ("-i", "--ip", default='localhost',help="IP address of broker/proxy")
    # add positional arguments in that order
    parser.add_argument ("topic", help="Topic")
    parser.add_argument ("id", help="ID")
    # parser.add_argument ("ownership", help="Ownership")
    # parser.add_argument ("history", help="History")
    # parse the args
    args = parser.parse_args ()
    return args

class Publisher():

    def __init__(self, args):
        self.args = args
        self.ip = getIP.get()
        self.config = configurator.load()
        zk = KazooClient(hosts=self.config['zkip']+':2181')
        self.zk = zk
        self.zk.start()
        self.rep_path = "/publishers/pub_" + self.args.id + '/rep_broker/ip/id'
        self.p_path = "/publishers/pub_" + self.args.id 
        onshp = self.args.ownership
        self.zk.ensure_path(self.rep_path)
        self.pub_tuple = (self.args.id + ',' + self.ip + ',' + self.args.topic + ',' + onshp + ',' + str(self.args.history)).encode('utf-8')
        self.zk.set(self.p_path,self.pub_tuple)
        @zk.DataWatch(self.rep_path)
        def watch_data(data, stat):
            print('leader change',data)
            self.setup_broker()
        
        


    def setup_broker(self):
        id = ''
        while len(id) == 0:
            id, znode_stats = self.zk.get(self.rep_path)
            id = id.decode('utf-8')
            print('my replicant ID: ' + id)
            time.sleep(2)

        repli_broker_ip, znode_stats = self.zk.get('/brokers/' + id + '/ip')
        repli_broker_ip = repli_broker_ip.decode('utf-8')

        
        
        
        self.context = zmq.Context()
        self.use_broker = self.config['use_broker']
    
        if self.use_broker:
            con_str = "tcp://" + repli_broker_ip + ":" + self.config['pub_port']
            print('Using broker @',con_str)
            self.socket = self.context.socket(zmq.PUB)
            self.socket.connect(con_str)
        else:
            # con_str = "tcp://" + self.ip + ":" + config['pub_port']
            print('Not using broker. Connecting to sdiscovery server @',repli_broker_ip)
            dclient = Dclient('PUB',self.args.topic,self.args.id,repli_broker_ip,self.ip)
            for i in range(1):
                discovery_server_response = dclient.broadcast()
            print('discovery_server_response',discovery_server_response)
            context = zmq.Context()
            # When not using broker, publisher publishes to localhost
            connect_str = "tcp://*:5556"   # changed 12:54
            self.socket = context.socket(zmq.PUB)
            self.socket.bind(connect_str)
            self.socket.send_string("yo yo yo this is a SETUP")
        # wait for friendly APIs to connect.
        time.sleep(2)

    def send(self, message):
        message =  self.args.topic + ' ,PUB,' + str(self.args.id) + ',' + message
        # print('sending',message)
        self.socket.send_string(message)
        # if self.use_broker:
        #     reply = self.socket.recv()
        #     return reply
        # else:
        #     return None


def main ():
    """ Main program for publisher. This will be the publishing application """
    args = parseCmdLineArgs()
    pub1 = Publisher(args)
    for i in range(20000):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S.%f")
        pub1.send(str(i) + ',' + current_time)
        # with open('log_pub_' + args.id + '_' + args.topic + '.out','a+') as fout:
        #     fout.write(str(i) + ',' + current_time + '\n')
        print(str(i) + ',' + current_time)
        sys.stdout.flush()
        time.sleep(2)


#----------------------------------------------
if __name__ == '__main__':
    main ()
