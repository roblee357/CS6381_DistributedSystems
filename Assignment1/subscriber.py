import sys, zmq, json

class Subscriber():
    def __init__(self, topic,sub_id):
        with open('config.json','r') as fin:
            config = json.load(fin)
        self.use_broker = config['use_broker']
        con_str = "tcp://" + config['ip'] + ":" + config['pub_port']
        self.topic = topic
        self.sub_id = sub_id
        # print('Creating the object')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.topicfilter = str.encode(self.topic)
        

        if self.use_broker:
            with open('config.json','r') as fin:
                config = json.load(fin)
            self.con_str = "tcp://" + config['ip'] + ":" + config['sub_port']
            self.socket.connect(self.con_str)
            self.socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)
        else:
            srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
            connect_str = "tcp://" + srv_addr + ":5556"
            print("Collecting updates from weather server proxy at: {}".format(connect_str))
            self.socket.connect(connect_str)
            print('topicfilter',self.topicfilter)
            self.socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)
            while True:
                string = self.socket.recv_string()
                print(string)

    def run(self):
        print('sub_id',self.sub_id,'subscribed to:' ,self.topic,'on', self.con_str)
        while True:
            string = self.socket.recv()
            if len(string)>0:
                return string

def main():
    sub1 = Subscriber('10001',1)
    # string = sub1.run()
    while True:
        reply = sub1.run()
        print(reply)

#----------------------------------------------
if __name__ == '__main__':
    main ()