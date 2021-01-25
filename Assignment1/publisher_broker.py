#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)
    decoded_message = message.decode("utf-8")
    if '_:_' in decoded_message:
        app_type = decoded_message.split('_:_')[0]
        ID = decoded_message.split('_:_')[1]
        topic = decoded_message.split('_:_')[2]
        
        print(app_type,topic,ID)


    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")