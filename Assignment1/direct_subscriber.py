import sys
import zmq
context = zmq.Context()
socket = context.socket(zmq.SUB)
connect_str = "tcp://10.0.0.8:5555"

socket.connect(connect_str)

# Subscribe to zipcode, default is NYC, 10001
zip_filter = "topic2"
print("Collecting updates from weather server...")
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

# Process 10 updates
while True:
   print('recieving')
   print(socket.recv_string())

