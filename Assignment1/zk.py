import time
import configurator
from kazoo.client import KazooClient   
import argparse 
from threading import Thread
import numpy as np
import math

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
        self.config = config
        self.zk_con_str = config['zkip']+':2181'
        print('connecting to ZK:' , self.zk_con_str)
        self.zk = KazooClient(hosts= self.zk_con_str,timeout=1)
        self.zk.start()
        self.b_path = "/brokers/broker_" + self.args.id 
        self.zk.delete(self.b_path,recursive=True)
        print('ip.encode(utf-8)',ip.encode('utf-8'))
        self.zk.create(self.b_path,value = ip.encode('utf-8'),ephemeral=True)
        self.zk.ensure_path("/publishers")

    def heartbeat(self):
        while True:
            heartbeat = (self.ip + ',' + str(time.time())).encode('utf-8')
            self.zk.set(self.b_path,heartbeat)
            time.sleep(self.config['broker_heartrate'])

    def start_heartbeat(self):
        t = Thread(target=self.heartbeat)
        t.start()  

    def get_topics(self):
        self.pub_dict = {}
        self.topics = {}
        publishers = self.zk.get_children("/publishers")
        for pub in publishers:
            self.pub_dict[pub] = {}
            data, zstat = self.zk.get("/publishers/" + pub)

            self.pub_dict[pub] = data.decode('utf-8')
            data_list = self.pub_dict[pub].split(',')
            if data_list[2] not in self.topics:
                self.topics[data_list[2]] = [pub]
            else:
                self.topics[data_list[2]].append(pub)
        print('pub_dict',self.pub_dict, 'topics', self.topics)

    def broker_replication_order(self):
        brokers = self.zk.get_children("/brokers")
        self.broker_order = []
        for broker in brokers:
            hb_time, znode_stats = self.zk.get("/brokers/" + broker)
            hb_str_time = hb_time.decode('utf-8')
            print('hb_str_time',hb_str_time)
            hb_flt_time = float(hb_str_time.split(',')[1])
            self.broker_order.append([broker,hb_flt_time])
            
            print('broker',broker, hb_time.decode('utf-8'))
        self.broker_order.sort(key=lambda x: x[1])
        print('self.broker_order',self.broker_order)




    def assign_broker(self):
        self.broker_replication_order()

        for i in range(len(self.broker_order)):
            print('self.broker_order[i]',self.broker_order[i])
            self.zk.ensure_path('/broker_order/' + str(i))
            self.zk.delete('/broker_order/' + str(i))
            broker = self.broker_order[i][0].split(',')[0].encode('utf-8')
            print('broker',broker)
            self.zk.create('/broker_order/' + str(i), value = broker, ephemeral=True )

        for topic in self.topics:
            broker_assignments = np.ceil((np.array(range(len(self.topics[topic])))+1)/self.config['load_topics_per_broker']).astype(int)
            print(broker_assignments, 'broker requirement', max(broker_assignments))
            i = 0
            for pub in self.topics[topic]: 
                
                rep_path = "/publishers/" + pub + '/rep_broker/ip/id'
                self.zk.ensure_path(rep_path)
                broker_name = self.broker_order[broker_assignments[i]][0]
                ip_node_path = '/brokers/' + broker_name 
                print(topic, pub,'broker_assignments',broker_assignments,'i',i,'ip_node_path',ip_node_path)
                ip, znode_stats = self.zk.get(ip_node_path)
                ip = ip.decode('utf-8').split(',')[0]
                self.zk.set("/publishers/" + pub + '/rep_broker/ip',ip)
                self.zk.set(rep_path,str(broker_name).encode('utf-8'))
                i += 1

    def load_ballance(self):
        while True:
            topics = self.get_topics()
            heartbeat = str(time.time()).encode('utf-8')
            self.zk.set(self.b_path,heartbeat)
            time.sleep(self.config['load_ballance_rate'])

    def start_load_ballancing(self):
        t = Thread(target=self.load_ballance)
        t.start() 

    def checkIfLeader(self):
        curTime = round(time.time()*1000)
        lead_broker, znode_stats = self.zk.get("/lead_broker")
        # print('lead_broker',lead_broker, 'znode_stats ', znode_stats)
        lead_broker_mtime = znode_stats[3]
        # print('lead_broker_mtime',lead_broker_mtime)
        lead_broker_age = curTime - lead_broker_mtime
        lead_broker_name = 'broker_' + lead_broker.decode('utf-8')
        # print('lead_broker_name', lead_broker_name,'lead_broker_age',lead_broker_age)
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
                    if leader_age > self.config["leader_timeout"]:
                        print('Leader is old. Let\'s get rid of they.', leader_age)
                        self.claim_lead()
                    else:
                        print('Leader is new.', leader_age)
            

    def continuousLeaderCheck(self):
        while True:
            self.checkIfLeader()
            time.sleep(self.config["leader_check_frequency"])

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
    zk.get_topics()
    zk.assign_broker()
    # zk.start_heartbeat()
    # # zk.claim_lead()
    # zk.checkIfLeader()
    # zk.start_leader_checks()

#----------------------------------------------
if __name__ == '__main__':
    main ()