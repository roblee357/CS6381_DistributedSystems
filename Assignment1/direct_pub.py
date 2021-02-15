import zmq
from random import randrange

print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

context = zmq.Context()

# The difference here is that this is a publisher and its aim in life is
# to just publish some value. The binding is as before.
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

# keep publishing 
while True:
    print()
    zipcode = 'topic2'
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)
    stupid_message = "%s %i %i" % (zipcode, temperature, relhumidity)
    print(stupid_message)
    socket.send_string(stupid_message)