import sys, zmq, json, argparse, time
from datetime import datetime

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
            config = json.load(fin)
        self.use_broker = config['use_broker']
        self.ip = ip
        self.con_str = "tcp://" + self.ip + ":" + config['sub_port']
        self.topic = topic
        self.sub_id = sub_id
        # print('Creating the object')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.topicfilter = str.encode(self.topic)
        print('topicfilter',self.topicfilter)
        # if self.use_broker:
        self.socket.connect(self.con_str)
        self.socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)
        # else:
        #     self.socket.connect(self.con_str)
        #     self.socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)

    def run(self):
        # print('sub_id',self.sub_id,'subscribed to:' ,self.topic,'on', self.con_str)
        while True:
            string = self.socket.recv()
            if len(string)>0:
                return string
            

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