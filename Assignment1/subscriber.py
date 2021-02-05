import sys, zmq, json

class Subscriber():
    def __init__(self, topic,sub_id):
        self.topic = topic
        self.sub_id = sub_id
        # print('Creating the object')
        context = zmq.Context()
        with open('config.json','r') as fin:
            config = json.load(fin)
        #  Socket to talk to server
        # print("Connecting to broker...")
        self.socket = context.socket(zmq.SUB)
        self.con_str = "tcp://" + config['ip'] + ":" + config['sub_port']
        # print(self.con_str)
        self.socket.connect(self.con_str)
        topicfilter = str.encode(self.topic)
        self.socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

    def run(self):
        # print('sub_id',self.sub_id,'subscribed to:' ,self.topic,'on', self.con_str)
        while True:
            string = self.socket.recv()
            if len(string)>0:
                return string
            # print(string)

# main
def main():
    sub1 = Subscriber('topic1',1)
    string = sub1.run()


#----------------------------------------------
if __name__ == '__main__':
    main ()