

import sys, zmq, json

class Subscriber():

    # def setup_socket(self,topic,sub_id):
    #     # Socket to talk to server
    #     with open('config.json','r') as fin:
    #         config = json.load(fin)

    #     context = zmq.Context()
    #     socket = context.socket(zmq.SUB)

    #     print("Socket setup...")

    #     bconnectionstring = str.encode('tcp://' + config['ip'] + ":" + config['port'])
    #     socket.connect (bconnectionstring)

    #     # Subscribe to zipcode, default is NYC, 10001
    #     topicfilter = str.encode(args.topic)
    #     socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
    #     return socket

    def __init__(self, topic,sub_id):
        self.topic = topic
        self.sub_id = sub_id
        print('Creating the object')
        context = zmq.Context()
        with open('config.json','r') as fin:
            config = json.load(fin)
        #  Socket to talk to server
        print("Connecting to broker...")
        self.socket = context.socket(zmq.SUB)
        self.con_str = "tcp://" + config['ip'] + ":" + config['port']
        print(self.con_str)
        self.socket.connect(self.con_str)
        topicfilter = str.encode(self.topic)
        self.socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
        ## Registering ## Commented out as each message is headered with pud_id and topic.
        # message = 'PUB_:_' + str(pub_id) + '_:_' + topic + '_:_registering'
        # register_reply = self.send(message)
        # print(register_reply)

    def run(self):
        print('sub_id',self.sub_id,'subscribed to:' ,self.topic,'on', self.con_str)
        while True:
            string = self.socket.recv()
            print(string)        

# main
def main():
    sub1 = Subscriber('topic1',1)
    sub1.run()


#----------------------------------------------
if __name__ == '__main__':
    main ()



