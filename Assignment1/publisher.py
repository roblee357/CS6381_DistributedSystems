import zmq,  json, sys
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
            print('Using broker')
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(con_str)
        else:
            print('Not using broker')
            context = zmq.Context()

            srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
            connect_str = "tcp://" + srv_addr + ":5555"

            # This is one of many potential publishers, and we are going
            # to send our publications to a proxy. So we use connect
            socket = context.socket(zmq.PUB)
            print ("Publisher connecting to proxy at: {}".format(connect_str))
            socket.connect(connect_str)

            # keep publishing 
            while True:
                zipcode = 10001 #randrange(1, 100000)
                temperature = 25 #randrange(-80, 135)
                relhumidity = 35 #randrange(10, 60)

                #print ("Sending: %i %i %i" % (zipcode, temperature, relhumidity))
                socket.send_string("%i %i %i" % (zipcode, temperature, relhumidity))


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
