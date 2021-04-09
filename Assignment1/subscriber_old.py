#
#   CS6381 Distributed Systems
#   Spring 2021
#   Assignment 1
#   Team 5 "El Sinko"
#   Rob Lee (robert.e.lee.1@vanderbilt.edu) and Jess Phelan (Jessica.phelan@vanderbilt.edu)
#   Publisher API
#

from discovery_client import *
import sys, zmq, json, argparse, time
from datetime import datetime
from multiprocessing.pool import ThreadPool
import configurator
import getIP
from kazoo.client import KazooClient
from threading import Thread
from timeout import timeout

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

def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()
    # add optional arguments
    # parser.add_argument ("-i", "--ip", default='localhost',help="IP address of broker/proxy")
    # add positional arguments in that order
    parser.add_argument ("topic", help="Topic")
    parser.add_argument ("id", help="ID")
    # parse the args
    args = parser.parse_args ()
    return args

class Subscriber():



    def __init__(self, args):
        self.topic = args.topic
        # self.context
        self.id = args.id
        self.ip = getIP.get() #ip
        self.config = configurator.load()
        self.socket = None
        self.socket_list=[]
        self.use_broker = self.config['use_broker']
        zk = KazooClient(hosts=self.config['zkip']+':2181')
        self.zk = zk
        self.zk.start()
        self.context = zmq.Context()
        self.running = True

        self.zk.ensure_path('/broker_topics')
        self.topics  = self.zk.get_children('/broker_topics')
        while not self.topic in self.topics:
            print('waiting for topic to be published...')
            time.sleep(2)
        
        @zk.DataWatch('/broker_topics/' + self.topic)
        def watch_data(data, stat):
            self.broker_ip = data.decode('utf-8')
            print('use broker' ,self.use_broker)
            if self.use_broker:
                self.con_str = "tcp://" + self.broker_ip + ":" + self.config['sub_port']
                self.createSocket()
                print('using broker',self.con_str)
            else:
                print('not using broker')
                self.get_sockets_from_discovery_server()


    def get_sockets_from_discovery_server(self):
            print('initiating discovery client connection')
            self.dclient = Dclient('SUB',self.topic,self.id,'localhost',self.ip,self.broker_ip)
            print('discovery client connection broadcast')
            discovery_server_response = self.dclient.broadcast()
            dicts = ': '.join(discovery_server_response.decode("utf-8").split(': ')[1:])
            print('dicts',dicts)
            try:
                pubs = json.loads(dicts)
                # for key in pubs.keys():
                key = list(pubs.keys())[0]
                print('pubs',pubs,'key',key)
                self.con_str = "tcp://" + pubs[key] + ":" + self.config['sub_port']
                print('key',key,'value',pubs[key], self.con_str)
                print("# starting loop")
                # self.socket_list.append(self.createSocket(self.con_str,self.topic))
                self.createSocket()
            except:
                print(dicts)

    def createSocket(self):
        
        self.socket = self.context.socket(zmq.SUB)
        self.topicfilter = str.encode(self.topic)
        self.socket.connect(self.con_str)
        self.socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)
        # Initialize poll set
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        time.sleep(.1)
        self.waitforsocketcreation = False
        self.running = True
        print('finished creating socket')

    @timeout(5)
    def get(self):
        self.i = 0
        if not self.use_broker:
            while self.socket == None:
                print('waiting for publishers...',self.i)
                self.i += 1
                time.sleep(1)
                self.get_sockets_from_discovery_server()
        if self.running:
            socks = dict(self.poller.poll())
            # print('socks',socks)
            if self.socket in socks:# and socks[self.socket] == zmq.POLLIN:
                response = self.socket.recv_string()
                return response
        else:
            print('not running')
            return None
            
def main():
    args = parseCmdLineArgs ()
    sub1 = Subscriber(args)
    print('# starting loop')
    sys.stdout.flush()
    start_time = datetime.now()
    last_time = start_time
    while True:
        try:
            reply = sub1.get()
        except:
            reply = None
            print('timeout')
        now = datetime.now()
        elapsed_time = str((now - start_time))
        cycle_time = str((now - last_time))
        last_time = now
        current_time = now.strftime("%H:%M:%S.%f")
        if not  reply is None:
            line_out = reply + ',' + current_time + ',' + elapsed_time + ',' + cycle_time 
        else:
            print('reply none type')
            line_out = 'None'
            time.sleep(1)
        print(line_out)
        sys.stdout.flush()
    print('exited')

#----------------------------------------------
if __name__ == '__main__':
    main ()