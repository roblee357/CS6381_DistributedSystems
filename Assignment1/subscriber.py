from discovery_client import *
import sys, zmq, json, argparse, time
from datetime import datetime
from multiprocessing.pool import ThreadPool
import configurator

def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()
    # add optional arguments
    parser.add_argument ("-i", "--ip", default='localhost',help="IP address of broker/proxy")
    # add positional arguments in that order
    parser.add_argument ("topic", help="Topic")
    parser.add_argument ("id", help="ID")
    # parse the args
    args = parser.parse_args ()
    return args

class Subscriber():
    def __init__(self, topic,sub_id,ip):
        self.config = configurator.load()
        self.use_broker = self.config['use_broker']
        self.topic = topic
        self.sub_id = sub_id
        self.ip = ip
        self.socket_obj = None
        self.socket_list=[]
        if self.use_broker:
            self.con_str = "tcp://" + ip + ":" + self.config['sub_port']
            self.socket_list.append(self.createSocket(self.con_str,self.topic))
        else:
            self.get_sockets_from_discovery_server()
        # self.socket = self.context.socket(zmq.SUB)
        # self.topicfilter = str.encode(self.topic)
        # print('topicfilter',self.topicfilter)
        # self.socket.connect(self.con_str)
        # self.socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)

    def get_sockets_from_discovery_server(self):
            print('initiating discovery client connection')
            self.dclient = Dclient('SUB',self.topic,self.sub_id,'localhost',self.ip)
            print('discovery client connection broadcast')
            discovery_server_response = self.dclient.broadcast()
            dicts = ': '.join(discovery_server_response.decode("utf-8").split(': ')[1:])
            print('dicts',dicts)
            try:
                pubs = json.loads(dicts)
                # for key in pubs.keys():
                key = list(pubs.keys())[0]
                print('pubs',pubs,'key',key)
                self.con_str = "tcp://" + pubs[key] + ":" + self.config['pub_port']
                print('key',key,'value',pubs[key], self.con_str)
                # self.socket_list.append(self.createSocket(self.con_str,self.topic))
                self.socket_obj = self.createSocket(self.con_str,self.topic)
            except:
                print(dicts)


    def createSocket(self, con_str,topicfilter):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        topicfilter = str.encode(topicfilter)
        socket.connect(con_str)
        socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
        return socket

    def listen(self, socket):
        while True:
            # print('waiting for message')
            message = socket.recv()
            if len(message)>0:
                return message

    def run(self,args):
        # pool = ThreadPool(processes=1)
        # print('len(self.socket_list)',len(self.socket_list))
        # with open('log_sub_' + args.id + '_' + args.topic + '.out','a+') as fout:
        #     fout.write('len(self.socket_list)' + str(len(self.socket_list) )+ '\n')
        self.i = 0
        # while len(self.socket_list) == 0 :
        while self.socket_obj == None:
            print('waiting for publishers...',self.i)
            self.i += 1
            time.sleep(1)
            self.get_sockets_from_discovery_server()


        # for socket in self.socket_list:
        #     # print(socket)
        #     # async_result = pool.apply_async(self.listen, (socket,)) # tuple of args for foo
        #     # response = async_result.get()
        #     # print('getting response')
        #     response = socket.recv_string()
        response = self.socket_obj.recv_string()
        return response



            
def main():
    args = parseCmdLineArgs ()
    sub1 = Subscriber(args.topic,args.id,args.ip)
    print('# starting loop')
    with open('log_sub_' + args.id + '_' + args.topic + '.out','a+') as fout:
        fout.write('# starting loop\n')
    start_time = datetime.now()
    last_time = start_time
    while True:
        reply = sub1.run(args)
        now = datetime.now()
        elapsed_time = str((now - start_time))
        cycle_time = str((now - last_time))
        last_time = now
        current_time = now.strftime("%H:%M:%S.%f")
        line_out = reply + ',' + current_time + ',' + elapsed_time + ',' + cycle_time 
        with open('log_sub_' + args.id + '_' + args.topic + '.out','a+') as fout:
            fout.write(line_out+ '\n')
        print(line_out)

#----------------------------------------------
if __name__ == '__main__':
    main ()