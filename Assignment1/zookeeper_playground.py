from kazoo.client import KazooClient
import json 
import time

with open('config.json','r') as fin:
    config = json.load(fin)
zk = KazooClient(hosts= config['zkip'] + ':2181')

zk.start()
data, stat = zk.get("/")
print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
brokerNo = '1'
b_path = "/electionpath/broker_" + brokerNo
zk.ensure_path(b_path)


heartbeat = str(time.time()).encode('utf-8')
zk.set(b_path,heartbeat)

data = zk.get(b_path)
print('data',data)
# zk.create("/electionpath", ephemeral=True, sequence=False)
# zk.set("/lead_broker/broker1",b"10.0.0.2")

# List the children
children = zk.get_children("/electionpath")
print("There are %s children with names %s" % (len(children), children))

# zk.create("/newer", ephemeral=False, sequence=False)

# election = zk.Election("/electionpath", "actor_1")

# def my_leader_function():
#     print('woohoo! I won')

# election.run(my_leader_function)