# Replicated brokers with ZooKeeper
## Leader elections: 
All brokers have a heartbeat.
The first broker to start writes it's name in the lead_broker znode.
The first replicated broker to realize the lead broker's age exceeds the timeout limit may claim lead broker seat.

1. Item 1
1. Item 2
1. Item 3
   1. Item 3a
   1. Item 3b

## Operation
 1. start ZooKeeper
    1. bin/zkServer.sh start
 1. ZooKeeper Visualizer
     1. ZooNavigator is a usefull dockerized server that helps visualize ZooKeeper
     1. docker pull elkozmon/zoonavigator
     1. docker run -d --network host -e HTTP_PORT=9000 --name zoonavigator --restart unless-stopped elkozmon/zoonavigator:latest 
     1. Go to http://localhost:9000.

   
 1. sudo python3 ps_mininet.py
     - Manual demo
    1. xterm s1h1  ...  xterm s1hn
    2. spawn some brokers: python3 dsorb.py topic1 1  ...n
    3. spawn some pubs and subs
    4. kill the lead / restart backups
    - Optional parameters
    1. -b  = broker mode - default=broker_on - try broker_off
    3. -B  = Brokers  - default = 3
    4. -P  = number of publishers - default = 3
    5. -S  = number of subscribers - default = 7

 2. source commands.txt 
 3. python3 performance_measuring.py 
 4. Review .png images of transit times. Note 90th, 95th, and 99th percentiles. 
<br>
## Diagram
 ![](images/Diagram.png?raw=true)<br>
<br>
<br>
<br>
# Results

## Brokered
 ![](images/With_broker_log_sub_h8s1.out_end-to-end.png?raw=true)<br>
The figure above shows 225 messages' transit times. This is using a proxy broker. The 99th percentile is 0.04728 seconds.
<br>
<br>
<br>
## Brokerless
 ![](images/Brokerless_log_sub_h8s1.out_end-to-end.png?raw=true)<br>
The figure above shows 243 messages' transit times. This is using a no broker, but rather a direct PUB/SUB connection that was match made by a discovery server. The 99th percentile is 0.03027 seconds.
