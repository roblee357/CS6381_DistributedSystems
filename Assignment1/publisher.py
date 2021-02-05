import zmq,  json 
import argparse

# https://python-patterns.guide/gang-of-four/singleton/
# What the Gang of Four’s original Singleton Pattern
# might look like in Python.

class Publisher():
    # _instance = None

    # def setup_socket(self,topic,pub_id):
    #     context = zmq.Context()
    #     with open('config.json','r') as fin:
    #         config = json.load(fin)
    #     #  Socket to talk to server
    #     print("Connecting to broker...")
    #     socket = context.socket(zmq.REQ)
    #     con_str = "tcp://" + config['ip'] + ":" + config['port']
    #     print(con_str)
    #     socket.connect(con_str)
    #     return socket

    def __init__(self, topic,pub_id):
        self.topic = topic
        self.pub_id = pub_id
        # print('Creating the object')
        context = zmq.Context()
        with open('config.json','r') as fin:
            config = json.load(fin)
        #  Socket to talk to server
        # print("Connecting to broker...")
        self.socket = context.socket(zmq.REQ)
        con_str = "tcp://" + config['ip'] + ":" + config['pub_port']
        # print(con_str)
        self.socket.connect(con_str)
        ## Registering ## Commented out as each message is headered with pud_id and topic.
        # message = 'PUB_:_' + str(pub_id) + '_:_' + topic + '_:_registering'
        # register_reply = self.send(message)
        # print(register_reply)

    def send(self, message):
        message = 'PUB_:_' + str(self.pub_id) + '_:_' + self.topic + '_:_' + message
        bmessage = str.encode(message)
        self.socket.send(bmessage)
        reply = self.socket.recv()
        # print(reply)
        return reply

def main ():
    """ Main program for publisher. This will be the publishing application """
    pub1 = Publisher('topic1',1)
    message = 'hello'
    reply = pub1.send(message)
    print(reply)

    pub2 = Publisher('topic2',2)
    message = 'hello again'
    reply = pub2.send(message)
    print(reply)

#----------------------------------------------
if __name__ == '__main__':
    main ()


# def register(socket, args):
#     print('Registering')
#     "Register-PUB-topic-1st_topic,SUB_ID=0"
#     message = 'Register_:_PUB_:_topic_:_' + args.topic + '_:_ID_:_' + str(args.id) + '_:_' +  args.message 
#     bmessage = str.encode(message)
#     socket.send(bmessage)
#     message = socket.recv()
#     socket.send(bmessage)
#     message = socket.recv()
#     print("Registration reply [ %s ]" % ( message))

# def parseCmdLineArgs ():
#     # parse the command line
#     parser = argparse.ArgumentParser ()
#     # optional arguments
#     parser.add_argument ("-bip", "--brokerip",  default='localhost', help="IP addr of broker")
#     parser.add_argument ("-bp", "--brokerport", type=int,  default=5555, help="IP addr of broker")
#     parser.add_argument ("-m", "--message",   default='word', help="message")
#     parser.add_argument ("-id", "--id", type=int,   default=0, help="ID (int)")
#     # # add positional arguments in that order
#     parser.add_argument ("topic", help="topic name")
#     # parser.add_argument ("masterip", help="IP addr of master")
#     # parser.add_argument ("brokerport", type=int, help="Port number of master")
#     # parse the args
#     args = parser.parse_args ()
#     return args

# def main ():
#     """ Main program for subscriber """
#     # first parse the command line arguments
#     args = parseCmdLineArgs ()
#     # setup socket with commandline arguments

#     socket = setup_socket(args)
#     # register(socket, args)
#     #  Do 10 requests, waiting each time for a response
#     for request in range(10):
#         message = 'Transmission_:_PUB_:_topic_:_' + args.topic + '_:_ID_:_' + str(args.id) + '_:_' +  args.message + ' ' + str(request)
#         # message = 'Transmission:_PUB_:_' + str(args.id) + '_:_' + args.topic + '_:_' + args.message 
#         reply = send(message)
#         #  Print the reply.
#         print("Received reply %s [ %s ]" % (request, reply))
    
# #----------------------------------------------
# if __name__ == '__main__':
#     main ()