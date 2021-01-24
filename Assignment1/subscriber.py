#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
print('subscriber started')
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to broker...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def register():
    print('Registering')
    socket.send(b"topic=1st_topic,subID=0")
    message = socket.recv()
    print("Registration reply [ %s ]" % ( message))

register()
register()

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s ..." % request)
    socket.send(b"Hello")

    #  Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))