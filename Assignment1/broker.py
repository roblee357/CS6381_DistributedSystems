#

#   Built from publisher.py hello world example
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# Dictionary for holding subcriber and publisher information
registry = {'PUB':[],'SUB':[]}

while True:
    #  Wait for next request from client
    message = socket.recv()
    # print("Received request: %s" % message)
    decoded_message = message.decode("utf-8")
    print(decoded_message)
    if '_:_' in decoded_message:
        deliminated_message = decoded_message.split('_:_')
        app_type = deliminated_message[1]
        ID = deliminated_message[5]
        topic = deliminated_message[3]
        print(app_type,topic,ID)
        if 'Register' in deliminated_message[0]:
            print('registering end point')
            if 'SUB' in deliminated_message[1]:
                # add ID and topic to set of registered subscribers as to not create duplicates 
                x = set(registry['SUB'])
                x.add(ID + ':' + topic)
                registry['SUB'] = x
                print('registry',registry)
                socket.send(b"Registered")
            if 'PUB' in deliminated_message[1]:
                # add ID and topic to set of registered subscribers as to not create duplicates 
                x = set(registry['SUB'])
                x.add(ID + ':' + topic)
                registry['SUB'] = x
                print('registry',registry)
                socket.send(b"Registered")   

        else:

            socket.send(b"Received") 

     


    #  Do some 'work'
    time.sleep(1)

    # #  Send reply back to client
    # socket.send(b"World")