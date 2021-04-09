import sys
from kazoo.client import KazooClient
import kazoo.recipe.watchers
import json 
import time


class ZK_Viewer:
    def __init__(self):
        with open('config.json','r') as fin:
            config = json.load(fin)
        self.zk = KazooClient(hosts= config['zkip'] + ':2181')

        self.zk.start()
        self.data_dict = {}
        self.line = ''

    def list_data(self,root, level=0):
        children = self.zk.get_children(root)
        i = 0
        for child in children:
            if (level == 0) and (i == 0):
                self.line = ''
            try:
                data, znode_stats = self.zk.get(root + "/" + child)
                data = data.decode('utf-8')

            
            
                indent = ' '*4*level
                # print(indent,child,data)
                self.line += indent + child + ' ' + data + '\n'
                self.data_dict[root + "/" + child] = {"data":data,"children":self.list_data(root + "/" + child, level = level + 1)}
                i += 1
            except:
                data = 'None'


def main():
    zkv = ZK_Viewer()
    while True:
        zkv.list_data('')
        # print(zkv.data_dict)
        for i in range(40):
            print('')
        print(zkv.line)

        # time.sleep(.1)

if __name__ == '__main__':
    main()


    # sys.stdout.write("\rDoing thing %s" % ','.join(children[:3]))
    # sys.stdout.flush()
    # time.sleep(.1)