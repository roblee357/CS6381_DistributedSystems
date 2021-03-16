import time
import configurator
from kazoo.client import KazooClient   
import argparse 
from threading import Thread

def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()
    # add positional arguments in that order
    parser.add_argument ("id", help="ID")
    args = parser.parse_args ()
    return args

class ZK:    
    def __init__(self,args, config, ip):
        self.args = args
        self.ip = ip
        self.zk = KazooClient(hosts= config['zkip']+':2181')
        self.zk.start()
        self.b_path = "/brokers/broker_" + self.args.id 
        self.ip_path = self.b_path + "/" + self.ip
        self.zk.ensure_path(self.ip_path)
        self.zk.ensure_path("/lead_broker/ip")

    def heartbeat(self):
        while True:
            heartbeat = str(time.time()).encode('utf-8')
            self.zk.set(self.b_path,heartbeat)
            time.sleep(.05)

    def start_heartbeat(self):
        t = Thread(target=self.heartbeat)
        t.start()  

    def checkIfLeader(self):
        curTime = round(time.time()*1000)
        lead_broker, znode_stats = self.zk.get("/lead_broker")
        print('lead_broker',lead_broker, 'znode_stats ', znode_stats)
        lead_broker_mtime = znode_stats[3]
        print('lead_broker_mtime',lead_broker_mtime)
        lead_broker_age = curTime - lead_broker_mtime
        lead_broker_name = 'broker_' + lead_broker.decode('utf-8')
        print('lead_broker_name', lead_broker_name,'lead_broker_age',lead_broker_age)
        brokers = self.zk.get_children("/brokers")
        if not lead_broker_name in brokers:
            print('broker not listed. Claiming lead',lead_broker_name, brokers)
            self.claim_lead()   
        else:
            for broker in brokers:
                broker_data, znode_stats = self.zk.get("/brokers/" + broker)
                mtime = znode_stats[3]
                print(lead_broker_name, broker, broker_data,mtime)
                if broker == lead_broker_name:
                    leader_age = curTime - mtime
                    if leader_age > 300:
                        print('Leader is old. Let\'s get rid of they.', leader_age)
                        self.claim_lead()
                    else:
                        print('Leader is new.', leader_age)
            

    def continuousLeaderCheck(self):
        while True:
            self.checkIfLeader()
            time.sleep(.5)

    def start_leader_checks(self):
        t = Thread(target=self.continuousLeaderCheck)
        t.start()          

    def claim_lead(self):
        if len(self.args.id.encode('utf-8')) > 0:
            self.zk.set("/lead_broker", self.args.id.encode('utf-8'))
            self.zk.set("/lead_broker/ip", self.ip.encode('utf-8'))
            print('lead claimed')
        else:
            print('trying to claim with null id')

def main():
    args = parseCmdLineArgs ()
    ip = '10.0.0.' + args.id
    config = configurator.load()
    zk = ZK(args, config, ip)
    zk.start_heartbeat()
    # zk.claim_lead()
    zk.checkIfLeader()
    zk.start_leader_checks()
    print('done')

#----------------------------------------------
if __name__ == '__main__':
    main ()