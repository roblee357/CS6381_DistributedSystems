import time, sys, random
import zmq

# Request - Reply socket for publishers
context = zmq.Context()
pub_socket = context.socket(zmq.REP)
pub_socket.bind("tcp://*:5555")

# Publish - Subscribe socket for subscribers
port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

#context = zmq.Context()
sub_socket = context.socket(zmq.PUB)
sub_socket.bind("tcp://*:%s" % port)


# Dictionary for holding subcriber and publisher information
registry = {'PUB':[],'SUB':[]}

while True:
    #  Wait for next request from client
    message = pub_socket.recv()
    # print("Received request: %s" % message)
    decoded_message = message.decode("utf-8")
    print(decoded_message)
    if '_:_' in decoded_message:
        deliminated_message = decoded_message.split('_:_')
        app_type = deliminated_message[0]
        ID = deliminated_message[1]
        topic = deliminated_message[2]
        message = deliminated_message[3]
        print(app_type,topic,ID,message)
      
        x = set(registry[app_type])
        # print('x',x,'registry[app_type]',registry[app_type])
        x.add(ID + ':' + topic)
        registry[app_type] = x
        print('registry',registry)

        messagedata = message #random.randrange(1,215) - 80
        print("%s %s" % (topic, messagedata))
        bmessage = str.encode(str(topic) + ' ' + str(messagedata))
        sub_socket.send(bmessage)
        
        pub_socket.send(b"Published " + bmessage)
    else:
        pub_socket.send(b"Published " + message)

    time.sleep(.01)