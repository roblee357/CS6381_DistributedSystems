from time import sleep
import configurator
from kazoo.client import KazooClient


class Zookeeper:
    def __init__(self, zookeeper_host):
        self.zookeeper_host = zookeeper_host
        

        self.zoo_client = KazooClient(hosts=f'{zookeeper_host}:2181')
        self.zoo_client.start()
        self.leader_observers = []

    # Get direct access to client for non-standard stuff
    def get_client(self):
        return self.zoo_client

    def add_leader_observer(self, callback):
        should_start = len(self.leader_observers) == 0
        self.leader_observers.append(callback)
        if should_start:
            self.start_observing_leader()

    def get_leader(self, i=0):
        values = self.zoo_client.get_children('/electionpath')
        values.sort()

        # fail-safe in case the publisher (or whomever) starts before broker
        if len(values) < 1:
            sleep(i + 1)
            return self.get_leader(i + 1)

        return values[0]

    # TODO: Watch the leader change!
    def get_leader_ip(self):
        leader = self.get_leader()
        node = self.zoo_client.get(f'/electionpath/{leader}')
        return node[0].decode('utf-8')

    def cleanup(self):
        self.zoo_client.stop()
        self.zoo_client.close()

    def watch_leader_changes(self, callback, leader=None):
        if leader is None:
            leader = self.get_leader()
        self.zoo_client.get(f'/electionpath/{leader}', watch=callback)

    # For help setting up new tests
    def delete_all(self):
        self.zoo_client.delete('/electionpath', -1, True)
        self.zoo_client.delete('/pubs', -1, True)
        self.zoo_client.delete('/subs', -1, True)

    def start_observing_leader(self):
        def watch_leader(data):
            leader = self.get_leader()
            
            self.watch_leader_changes(watch_leader, leader)
            for observer in self.leader_observers:
                observer()
        
        leader = self.get_leader()
        self.watch_leader_changes(watch_leader, leader)
        for observer in self.leader_observers:
            observer()


def main():
    config = configurator.load()
    print(config['zkip'])
    zk = Zookeeper(config['zkip'] )
    print('leader IP',zk.get_leader_ip())
    


#----------------------------------------------
if __name__ == '__main__':
    main ()