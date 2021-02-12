import zmq,  json, sys
import argparse, time

def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()
    # add optional arguments
    parser.add_argument ("-i", "--ip", default='localhost',help="IP address of broker/proxy")
    parser.add_argument ("-s", "--sip", default='localhost',help="IP address of discovery server")
    # add positional arguments in that order
    parser.add_argument ("topic", help="Topic")
    parser.add_argument ("id", help="ID")
    # parse the args
    args = parser.parse_args ()
    return args

class Dclient():

    def __init__(self, ispub, topic,pub_id,ip,sip):
        self.ispub = ispub
        self.topic = topic
        self.pub_id = pub_id
        self.ip = ip
        self.sip = sip #server IP
        self.context = zmq.Context()
        with open('config.json','r') as fin:
            config = json.load(fin)
        self.dip = config['dip']
        self.port = config['disc_port']
        con_str = "tcp://" + self.dip + ":" + self.port
        print(con_str)
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(con_str)
        time.sleep(.5)

    def broadcast(self):
        message =  self.ispub + ',' +self.topic + ',' + str(self.pub_id) + ',' + str(self.sip)
        # print('dclient sending',message)
        self.socket.send_string(message)
        reply = self.socket.recv()
        # print('dclient recieved',reply)
        return reply

def main ():
    """ Main program for publisher. This will be the publishing application """
    args = parseCmdLineArgs ()
    dclient = Dclient('PUB',args.topic,args.id,args.ip,args.sip)
    for i in range(1):
        discovery_server_response = dclient.broadcast()
    print('discovery_server_response',discovery_server_response)

    dclient2 = Dclient('PUB','topic2','2','localhost','10.0.0.2')
    for i in range(1):
        discovery_server_response = dclient2.broadcast()
    print('discovery_server_response',discovery_server_response)

    dclient3 = Dclient('PUB','topic2','3','localhost','10.0.0.3')
    for i in range(1):
        discovery_server_response = dclient3.broadcast()
    print('discovery_server_response',discovery_server_response)

    dclient4 = Dclient('SUB','topic2','4','localhost','10.0.0.3')
    for i in range(1):
        discovery_server_response = dclient4.broadcast()
    print('discovery_server_response',discovery_server_response)

#----------------------------------------------
if __name__ == '__main__':
    main ()
