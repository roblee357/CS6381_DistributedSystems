import zmq,  json 
import argparse

class Publisher():

    def __init__(self, topic,pub_id):
        self.topic = topic
        self.pub_id = pub_id
        self.context = zmq.Context()
        with open('config.json','r') as fin:
            config = json.load(fin)
        self.use_broker = config['use_broker']
        con_str = "tcp://" + config['ip'] + ":" + config['pub_port']
        if self.use_broker:
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(con_str)
        else:
            con_str = "tcp://*:" + config['sub_port']
            self.socket = self.context.socket(zmq.PUB)
            self.socket.bind("tcp://*:%s" % config['sub_port'])


    def send(self, message):
        message = 'PUB_:_' + str(self.pub_id) + '_:_' + self.topic + '_:_' + message
        bmessage = str.encode(message)
        self.socket.send(bmessage)
        if self.use_broker:
            reply = self.socket.recv()
            return reply
        else:
            reply = "one way message"
            return reply


def main ():
    """ Main program for publisher. This will be the publishing application """
    pub1 = Publisher('topic1',1)
    message = 'hello...........................................'
    reply = pub1.send(message)
    print(reply)

    pub2 = Publisher('topic2',2)
    message = 'hello again....................................'
    reply = pub2.send(message)
    print(reply)

#----------------------------------------------
if __name__ == '__main__':
    main ()
