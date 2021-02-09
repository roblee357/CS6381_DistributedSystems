import zmq,  json, sys
import argparse, time

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
            print('Using broker')
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(con_str)
        else:
            print('Not using broker')
            context = zmq.Context()
            srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
            connect_str = "tcp://" + srv_addr + ":5555"
            self.socket = context.socket(zmq.PUB)
            print ("Publisher connecting to proxy at: {}".format(connect_str))
            self.socket.connect(connect_str)
            self.socket.send_string("yo yo yo this is a SETUP")
        # wait for friendly APIs to connect.
        time.sleep(.5)


    def send(self, message):
        message =  self.topic + ' _:_PUB_:_' + str(self.pub_id) + '_:_' + message

        if self.use_broker:
            # bmessage = str.encode(message)
            self.socket.send_string(message)
            reply = self.socket.recv()
            return reply
        else:
            self.socket.send_string(message )
            time.sleep(.05)


def main ():
    """ Main program for publisher. This will be the publishing application """
    pub1 = Publisher('10001',3)
    message = "now THIS is a message"
    reply = pub1.send(message)
    print(reply)

    pub2 = Publisher('topic2',4)
    message = "messy message"
    reply = pub2.send(message)
    print(reply)

#----------------------------------------------
if __name__ == '__main__':
    main ()
