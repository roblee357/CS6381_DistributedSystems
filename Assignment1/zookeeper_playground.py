from kazoo.client import KazooClient
import kazoo.recipe.watchers
import json 
import time

with open('config.json','r') as fin:
    config = json.load(fin)
zk = KazooClient(hosts= config['zkip'] + ':2181')

zk.start()
data, stat = zk.get("/")
print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))


watcher = kazoo.recipe.watchers.PatientChildrenWatch(zk, '/publishers',
                               time_boundary=5)
async_object = watcher.start()

# Blocks until the children have not changed for time boundary
# (5 in this case) seconds, returns children list and an
# async_result that will be set if the children change in the
# future
children, child_async = async_object.get()

print('children', 'child_async', children, child_async)

# List the children
children = zk.get_children("/electionpath")
print("There are %s children with names %s" % (len(children), children))

# zk.create("/newer", ephemeral=False, sequence=False)

# election = zk.Election("/electionpath", "actor_1")

# def my_leader_function():
#     print('woohoo! I won')

# election.run(my_leader_function)