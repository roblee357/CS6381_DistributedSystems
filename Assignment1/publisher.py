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
import configurator, getIP

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
    parser.add_argument ("-m", "--mes", default='Hello World',help="The Message")
    parser.add_argument ("-i", "--ip", default='localhost',help="IP address of broker/proxy")
    # add positional arguments in that order
    parser.add_argument ("topic", help="Topic")
    parser.add_argument ("id", help="ID")
    # parse the args
    args = parser.parse_args ()
    return args

class Publisher():

    def __init__(self, topic,pub_id,ip):
        self.topic = topic
        self.pub_id = pub_id
        self.ip = getIP.get() #ip
        self.context = zmq.Context()
        config = configurator.load()
        
        self.use_broker = config['use_broker']
        
        if self.use_broker:
            con_str = "tcp://" + config['dip'] + ":" + config['pub_port']
            print('Using broker @',con_str)
            self.socket = self.context.socket(zmq.PUB)
            self.socket.connect(con_str)
        else:
            # con_str = "tcp://" + self.ip + ":" + config['pub_port']
            print('Not using broker. Connecting to sdiscovery server @',config['dip'])
            dclient = Dclient('PUB',self.topic,self.pub_id,config['dip'],self.ip)
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
        message =  self.topic + ' ,PUB,' + str(self.pub_id) + ',' + message
        # print('sending',message)
        self.socket.send_string(message)
        # if self.use_broker:
        #     reply = self.socket.recv()
        #     return reply
        # else:
        #     return None


def main ():
    """ Main program for publisher. This will be the publishing application """
    args = parseCmdLineArgs ()
    pub1 = Publisher(args.topic,args.id,args.ip)
    for i in range(200):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S.%f")
        pub1.send(str(i) + ',' + current_time)
        # with open('log_pub_' + args.id + '_' + args.topic + '.out','a+') as fout:
        #     fout.write(str(i) + ',' + current_time + '\n')
        print(str(i) + ',' + current_time)
        sys.stdout.flush()
        time.sleep(.01)


#----------------------------------------------
if __name__ == '__main__':
    main ()
