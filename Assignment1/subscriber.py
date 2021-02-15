from discovery_client import *
import sys, zmq, json, argparse, time
from datetime import datetime
from multiprocessing.pool import ThreadPool

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
        with open('config.json','r') as fin:
            self.config = json.load(fin)
        self.use_broker = self.config['use_broker']
        self.topic = topic
        self.sub_id = sub_id
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
            self.dclient = Dclient('SUB',self.topic,self.sub_id,'localhost',self.config['dip'])
            print('discovery client connection broadcast')
            discovery_server_response = self.dclient.broadcast()
            dicts = ': '.join(discovery_server_response.decode("utf-8").split(': ')[1:])
            print('dicts',dicts)
            try:
                pubs = json.loads(dicts)
                for key in pubs.keys():
                    
                    self.con_str = "tcp://" + pubs[key] + ":" + self.config['pub_port']
                    print('key',key,'value',pubs[key], self.con_str)
                    self.socket_list.append(self.createSocket(self.con_str,self.topic))
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
        t = 0
        while True:
            print('waiting for message')
            message = socket.recv()
            if len(message)>0:
                return message
            # t += 1
            # returnification_string = "this is the return string " + str(t)
            # return returnification_string

    def run(self):
        pool = ThreadPool(processes=1)
        print('len(self.socket_list)',len(self.socket_list))
        self.i = 0
        while len(self.socket_list) == 0 :
            print('waiting for publishers...',self.i)
            self.i += 1
            time.sleep(1)
            self.get_sockets_from_discovery_server()


        for socket in self.socket_list:
            # print(socket)
            async_result = pool.apply_async(self.listen, (socket,)) # tuple of args for foo
            response = async_result.get()
            print('getting response')
            response = socket.recv_string()
        return response
            # t = Thread(target=self.listen)
            # t.daemon = True
            # t.start()


            
def main():
    args = parseCmdLineArgs ()
    sub1 = Subscriber(args.topic,args.id,args.ip)
    # string = sub1.run()
    print('starting loop')
    start_time = datetime.now()
    last_time = start_time
    while True:
        reply = sub1.run()
        now = datetime.now()
        elapsed_time = str((now - start_time))
        cycle_time = str((now - last_time))
        last_time = now
        current_time = now.strftime("%H:%M:%S.%f")
        # with open('sub_log_' + args.id + '_' + args.topic + '.txt','a+') as fout:
        #     fout.write(reply + '_' + current_time + '_' + elapsed_time + '_' + cycle_time + '\n')
        print(reply + ',' + current_time + ',' + elapsed_time + ',' + cycle_time)

#----------------------------------------------
if __name__ == '__main__':
    main ()