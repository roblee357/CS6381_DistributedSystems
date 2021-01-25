#   
#   Team 
#   Jess and Rob
# 
#
#   Broker in Python
#


print('Broker started')
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

# Define a blank dictionary to hold IDs of applications
blank_dict = {}

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)
    decoded_message = message.decode("utf-8")
    if 'topic' in decoded_message:
        topic = decoded_message.split(',')[0].split('=')[1]
        ID = decoded_message.split(',')[1].split('=')[1]
        app_type = decoded_message.split(',')[1][:3]
        print(app_type,topic,ID)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")