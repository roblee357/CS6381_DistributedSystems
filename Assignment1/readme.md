# Assignment 1 message broker
 
 At this point, subscriber.py can talk to publisher_broker sending the following parameters in a message.
 1. Application type (SUB/PUB)
 2. ID (int)
 3. Topic
 4. Message

 While there are some other examples in this folder like expresso.py and zmqpolling.py, this work has only used the hello world example from class. 

 Argparse is used to parse commandline arguments.
 The broker and subscriber can be started in any order. 
 On my system I start the broker with this command:
 * /usr/bin/python3 /home/v2-local/Desktop/CS6381_DistributedSystems/Assignment1/publisher.py
 and the subscriber with this:
 * python3 subscriber.py 2nd_topic -m 'Here we go again!' -sid 4
 1. "2nd_topic" is the topic 
 2. 'Here we go again!' is the message
 3. 4 is the ID 
