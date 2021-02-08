import zmq
import threading

# So that you can copy-and-paste this into an interactive session, I'm
# using threading, but obviously that's not what you'd use

# I'm the subscriber that multiple clients are writing to
def parent():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b'Child:')
    # Even though I'm the subscriber, I'm allowed to get this party 
    # started with `bind`
    socket.bind('tcp://127.0.0.1:5000')

    # I expect 50 messages
    for i in range(50):
        print ('Parent received: %s' % socket.recv())

# I'm a child publisher
def child(number):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    # And even though I'm the publisher, I can do the connecting rather
    # than the binding
    socket.connect('tcp://127.0.0.1:5000')

    for data in range(5):
        socket.send(b'Child: %i %i' % (number, data))
    socket.close()

threads = [threading.Thread(target=parent)] + [threading.Thread(target=child, args=(i,)) for i in range(10)]
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()