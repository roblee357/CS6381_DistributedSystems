#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
print('subscriber started')
import zmq, argparse 


def setup_socket(args):

    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to broker...")
    socket = context.socket(zmq.REQ)
    con_str = "tcp://" + args.brokerip + ":" + str(args.brokerport)
    print(con_str)
    socket.connect(con_str)
    return socket

def register(socket):
    print('Registering')
    socket.send(b"topic=1st_topic,SUB_ID=0")
    message = socket.recv()
    print("Registration reply [ %s ]" % ( message))



def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()

    # optional arguments
    parser.add_argument ("-bip", "--brokerip",  default='localhost', help="IP addr of broker")
    parser.add_argument ("-bp", "--brokerport", type=int,  default=5555, help="IP addr of broker")
    parser.add_argument ("-m", "--message",   default='word', help="message")
    parser.add_argument ("-sid", "--subid", type=int,   default=0, help="Subscriber ID (int)")

    # # add positional arguments in that order
    parser.add_argument ("topic", help="topic name")
    # parser.add_argument ("masterip", help="IP addr of master")
    # parser.add_argument ("brokerport", type=int, help="Port number of master")
    # parse the args
    args = parser.parse_args ()
    return args






def main ():
    """ Main program for subscriber """
    
    # first parse the command line arguments
    args = parseCmdLineArgs ()
    # setup socket with commandline arguments
    socket = setup_socket(args)
    register(socket)
    #  Do 10 requests, waiting each time for a response
    for request in range(10):
        print("Sending request %s ..." % request)
        message = 'SUB_:_' + str(args.subid) + '_:_' + args.topic + '_:_' + args.message 
        bmessage = str.encode(message)
        socket.send(bmessage)

        #  Get the reply.
        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))
    
#----------------------------------------------
if __name__ == '__main__':
    main ()