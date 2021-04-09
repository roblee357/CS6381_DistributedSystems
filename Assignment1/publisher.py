from discovery_client import *
import zmq,  json, sys
import argparse, time
from datetime import datetime
import configurator
from kazoo.client import KazooClient
import getIP
import watchers
import random, math
from zk import ZK


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
        zk = KazooClient(hosts=self.config['zkip']+':2181',timeout=1)
        self.zk = zk
        self.zk.start()
        self.broker_order_path = "/broker_order"
        self.publisher_path = "/publisher_order"
        self.p_path = "/publishers/pub_" + self.args.id 
        onshp = self.args.ownership
        self.zk.ensure_path(self.p_path)
        self.zk.ensure_path(self.broker_order_path)
        self.zk.ensure_path('/publisher_topic_registration')
        self.pub_tuple = (self.args.id + ',' + self.ip + ',' + self.args.topic + ',' + onshp + ',' + str(self.args.history)).encode('utf-8')
        self.zk.delete(self.p_path)
        self.zk.create(self.p_path,value=self.pub_tuple,ephemeral=True)
        # self.zk.set(self.p_path,self.pub_tuple)
        self.register_topic()
        self.broker_topic_path = '/broker_topics/' + self.args.topic
        self.zk.ensure_path(self.broker_topic_path )
        # self.broker_topic_data = 0
        @zk.DataWatch(self.broker_topic_path)
        def watch_data(data, stat):
            if not data is None:
                if len(data) > 0:
                    self.broker_topic_data = data

                    # if not first_pass is None:
                    print('woah, something changed with el broker noderino ' + self.broker_topic_path , 'data' , data)
                        # if not data is None:
                        #     if len(data)>0:
                        #         self.broker_topic_data = data
                    self.broker_topic_data = data
                    self.get_broker()       
            else:
                while (data is None) or (len(data) == 0):
                    try:
                        self.broker_topic_data, znode_stats = self.zk.get(self.broker_topic_path)
                    except:
                        print('could not get broker_topic node data')
                    print('waiting for broker_topic assignment...')
                    time.sleep(2)
                self.get_broker()


    def register_topic(self):
        topics = self.zk.get_children('/publisher_topic_registration')
        pub_data = (self.args.ownership + ',' + str(self.args.history) + ',' + self.args.id ).encode('utf-8')

        def create_topic_node():
            self.zk.create('/publisher_topic_registration/' + self.args.topic, ephemeral=True)
            topics = self.zk.get_children('/publisher_topic_registration')
            self.zk.set('/publisher_topic_registration/' + self.args.topic,pub_data)

        # if the topic already exists check ownership strength
        if len(topics) == 0 :
            create_topic_node()
        else:
            if not self.args.topic in topics:
                create_topic_node()

            # Topic already exists...
            else:
            # Check ownership
                data, znode_stats = self.zk.get('/publisher_topic_registration/' + self.args.topic)
                data = data.decode('utf-8')
                ownership , history , pub_id = data.split(',')
                ownership , history = float(ownership) , int(history)
                print('topic exists ownership', ownership, 'my ownership', self.args.ownership)
                if  float(self.args.ownership) > ownership:
                    # Take owning topic position
                    self.zk.set('/publisher_topic_registration/' + self.args.topic,pub_data)

    def get_broker(self):
        pub_info = self.broker_topic_data.decode('utf-8').split(',')
        print('pub_info',pub_info,'self.args.id',self.args.id) #,self.args.id==pub_info[1])
        repli_broker_ip = pub_info[0]
        owning_pub = pub_info[1]
        if owning_pub == self.args.id:
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
        else:            
            print('not owning pub')
            time.sleep(2)
            self.socket = None
            self.register_topic()
            self.broker_topic_data, znode_stats = self.zk.get(self.broker_topic_path)
            self.get_broker()
            

    def send(self, message):
        if hasattr(self,'socket'):
            if not self.socket is None:
                message =  self.args.topic + ' ,PUB,' + str(self.args.id) + ',' + message
                self.socket.send_string(message)
        else:
            print("socket is None. May not be owning topic.")

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
