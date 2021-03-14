from kazoo.client import KazooClient

zk = KazooClient(hosts='172.17.0.1:2181')
zk.stop()
zk.start()
data, stat = zk.get("/")
print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

election = zk.Election("/electionpath", "actor_1")

def my_leader_function():
    print('woohoo! I won')

election.run(my_leader_function)




# zk.create("/electionpath", ephemeral=False, sequence=False)
# zk.set("/lead_broker/broker1",b"10.0.0.2")

# List the children
children = zk.get_children("/lead_broker")
print("There are %s children with names %s" % (len(children), children))

# zk.create("/newer", ephemeral=False, sequence=False)