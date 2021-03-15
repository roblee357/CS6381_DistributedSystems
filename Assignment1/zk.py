import time
import configurator
from kazoo.client import KazooClient   
import argparse 

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
 
        # zk.create("/electionpath", ephemeral=False, sequence=False)
        # try:
        #     self.zk.delete("/lead_broker",recursive=True)
        # except:
        #     print("no leader zNode")
        # self.zk.ensure_path("/lead_broker/broker" + str(self.args.id))
        # self.zk.set("/lead_broker/broker" + str(self.args.id),bytes(self.ip,'utf-8'))

    def heartbeat(self):
        b_path = "/electionpath/broker_" + self.args.id
        self.zk.ensure_path(b_path)
        heartbeat = str(time.time()).encode('utf-8')
        self.zk.set(b_path,heartbeat)


    def checkIfLeader(self):
        curTime = round(time.time()*1000)
        lead_broker, znode_stats = self.zk.get("/lead_broker")
        print('lead_broker',lead_broker, 'znode_stats ', znode_stats)
        lead_broker_mtime = znode_stats[3]
        print('lead_broker_mtime',lead_broker_mtime)
        lead_broker_age = curTime - lead_broker_mtime
        lead_broker_name = 'broker_' + lead_broker.decode('utf-8')
        print('lead_broker_name', lead_broker_name,'lead_broker_age',lead_broker_age)
        brokers = self.zk.get_children("/electionpath")

        for broker in brokers:
            broker_data, znode_stats = self.zk.get("/electionpath/" + broker)
            mtime = znode_stats[3]
            print(lead_broker_name, broker, broker_data,mtime)
            if broker == lead_broker_name:
                leader_age = curTime - mtime
                if leader_age > 300:
                    print('Leader is old. Let\'s get rid of they.', leader_age)
                    self.claim_lead()
                else:
                    print('Leader is new.', leader_age)


    def claim_lead(self):
        self.zk.set("/lead_broker", self.args.id.encode('utf-8'))
        print('lead claimed')

def main():
    args = parseCmdLineArgs ()
    ip = '10.0.0.' + args.id
    config = configurator.load()
    zk = ZK(args, config, ip)
    zk.heartbeat()
    # zk.claim_lead()
    zk.checkIfLeader()

#----------------------------------------------
if __name__ == '__main__':
    main ()