# Assignment 1 message broker

 1. sudo mn -x --link=tc --topo=tree,fanout=3,depth=2
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


![diagram](roblee357/CS6381_DistributedSystems/blob/main/Assignment1/jess/setup-diagram.png)

Note: The discovery files in Assignment1 work for the "brokerless" approach.

The file "discovery_server_OR_broker.py" combines the broker and the discovery server approach.
