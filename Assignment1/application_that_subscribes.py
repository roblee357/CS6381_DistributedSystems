from discovery_client import *
import sys, zmq, json, argparse, time
from datetime import datetime
from multiprocessing.pool import ThreadPool
import configurator
import getIP
from kazoo.client import KazooClient
from threading import Thread
from timeout import timeout
from subscriber import Subscriber

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()
    # add optional arguments
    # parser.add_argument ("-i", "--ip", default='localhost',help="IP address of broker/proxy")
    # add positional arguments in that order
    parser.add_argument ("topic", help="Topic")
    parser.add_argument ("id", help="ID")
    # parse the args
    args = parser.parse_args ()
    return args


def main():
    args = parseCmdLineArgs ()
    sub1 = Subscriber(args)
    print('# starting loop')
    sys.stdout.flush()
    start_time = datetime.now()
    last_time = start_time
    while True:
        try:
            reply = sub1.get()
        except:
            reply = None
            print('timeout')
        now = datetime.now()
        elapsed_time = str((now - start_time))
        cycle_time = str((now - last_time))
        last_time = now
        current_time = now.strftime("%H:%M:%S.%f")
        if not  reply is None:
            line_out = reply + ',' + current_time + ',' + elapsed_time + ',' + cycle_time 
        else:
            print('reply none type')
            line_out = 'None'
            time.sleep(1)
        print(line_out)
        sys.stdout.flush()
    print('exited')

#----------------------------------------------
if __name__ == '__main__':
    main ()