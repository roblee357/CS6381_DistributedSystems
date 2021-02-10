import zmq,  json, sys
import argparse, time

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

class Publisher():

    def __init__(self, topic,pub_id,ip):
        self.topic = topic
        self.pub_id = pub_id
        self.ip = ip
        self.context = zmq.Context()
        with open('config.json','r') as fin:
            config = json.load(fin)
        self.use_broker = config['use_broker']
        con_str = "tcp://" + self.ip + ":" + config['pub_port']
        if self.use_broker:
            print('Using broker')
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(con_str)
            
        else:
            print('Not using broker')
            context = zmq.Context()
            connect_str = "tcp://" + self.ip + ":5555"
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
    args = parseCmdLineArgs ()
    pub1 = Publisher(args.topic,args.id,args.ip)
    message = "now THIS is a message"
    reply = pub1.send(message)
    print(reply)

    pub2 = Publisher('topic2',4,'10.0.0.1')
    message = "messy message"
    reply = pub2.send(message)
    print(reply)

#----------------------------------------------
if __name__ == '__main__':
    main ()
