import sys, argparse
import zmq

def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()
    # optional arguments
    parser.add_argument ("-bip", "--brokerip",  default='localhost', help="IP addr of broker")
    parser.add_argument ("-bp", "--brokerport",   default='5556', help="IP addr of broker")
    parser.add_argument ("-m", "--message",   default='word', help="message")
    parser.add_argument ("-id", "--id", type=int,   default=0, help="ID (int)")
    # # add positional arguments in that order
    parser.add_argument ("topic", help="topic name")
    # parse the args
    args = parser.parse_args ()
    return args

def setup_socket(args):
    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    bconnectionstring = str.encode('tcp://' +  args.brokerip  + ':' + args.brokerport)
    socket.connect (bconnectionstring)
    # Subscribe to zipcode, default is NYC, 10001
    topicfilter = str.encode(args.topic)
    socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
    return socket

# main
def main():
    # first parse the command line arguments
    args = parseCmdLineArgs ()
    # setup socket with commandline arguments
    socket = setup_socket(args)
    total_value = 0
    while True:
        string = socket.recv()
        print(string)

#----------------------------------------------
if __name__ == '__main__':
    main ()