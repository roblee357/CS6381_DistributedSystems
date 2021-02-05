import zmq, time, sys, random
from  multiprocessing import Process

from publisher import *
from subscriber import *
from broker import *


def start_broker():
    print('broker starting')
    broker = Broker()
    broker.run()
    
def create_publishers():
    print('creating pub1 ')
    pub1 = Publisher('topic1',3)
    print('creating pub2 ')
    pub2 = Publisher('topic2',2)
    while True:
        time.sleep(1)
        reply = pub1.send('hello')
        print(reply)
        message = 'hello again'
        reply = pub2.send(message)
        print(reply)

def create_subscribers1():
    print('creating sub1 ')
    sub1 = Subscriber('topic1',3)
    while True:
        reply = sub1.run()
        print('subscriber 1 ' , reply)

def create_subscribers2():
    print('creating sub2 ')
    sub2 = Subscriber('topic2',3)
    print('subscribers started')
    while True:
        reply = sub2.run()
        print('subscriber 2 ' , reply)
        
if __name__ == "__main__":
    print('starting broker process')
    Process(target=start_broker).start()
    print('creating publishers process')
    Process(target=create_publishers).start()
    print('creating subscribers process')
    Process(target=create_subscribers1).start()
    print('starting subscribers')
    Process(target=create_subscribers2).start()
    print('process started')

# reply = pub1.send('hello pub1 2')
# print(reply)

# def server_push(port="5556"):
#     context = zmq.Context()
#     socket = context.socket(zmq.PUSH)
#     socket.bind("tcp://*:%s" % port)
#     print ("Running server on port: ", port)
#     # serves only 5 request and dies
#     for reqnum in range(10):
#         if reqnum < 6:
#             socket.send(b"Continue")
#         else:
#             socket.send(b"Exit")
#             break
#         time.sleep (1) 

# def server_pub(port="5558"):
#     context = zmq.Context()
#     socket = context.socket(zmq.PUB)
#     socket.bind("tcp://*:%s" % port)
#     publisher_id = random.randrange(0,9999)
#     print ("Running server on port: ", port)
#     # serves only 5 request and dies
#     for reqnum in range(10):
#         # Wait for next request from client
#         topic = random.randrange(8,10)
#         messagedata = "server#%s" % publisher_id
#         print ("%s %s" % (topic, messagedata))
#         socket.send(str.encode("%d %s" % (topic, messagedata)))
#         time.sleep(1)    

# def client(port_push, port_sub):
#     context = zmq.Context()
#     socket_pull = context.socket(zmq.PULL)
#     socket_pull.connect ("tcp://localhost:%s" % port_push)
#     print ("Connected to server with port %s" % port_push)
#     socket_sub = context.socket(zmq.SUB)
#     socket_sub.connect ("tcp://localhost:%s" % port_sub)
#     socket_sub.setsockopt(zmq.SUBSCRIBE, b"9")
#     print ("Connected to publisher with port %s" % port_sub)
#     # Initialize poll set
#     poller = zmq.Poller()
#     poller.register(socket_pull, zmq.POLLIN)
#     poller.register(socket_sub, zmq.POLLIN)

#     # Work on requests from both server and publisher
#     should_continue = True
#     while should_continue:
#         socks = dict(poller.poll())
#         if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
#             message = socket_pull.recv()
#             print ("Recieved control command: %s" % message)
#             if message == "Exit": 
#                 print ("Recieved exit command, client will stop recieving messages")
#                 should_continue = False

#         if socket_sub in socks and socks[socket_sub] == zmq.POLLIN:
#             string = socket_sub.recv()
#             topic, messagedata = string.split()
#             print ("Processing ... ", topic, messagedata)


# print('starting')
# if __name__ == "__main__":
#     # Now we can run a few servers 
#     server_push_port = "5556"
#     server_pub_port = "5558"
#     print('starting')
#     Process(target=server_push, args=(server_push_port,)).start()
#     Process(target=server_pub, args=(server_pub_port,)).start()
#     Process(target=client, args=(server_push_port,server_pub_port,)).start()