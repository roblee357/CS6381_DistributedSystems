import zmq, time, sys, random
from  multiprocessing import Process

from publisher import *
from subscriber import *
from broker import *
from configurator import *

change('use_broker',True)

def start_broker():
    print('broker starting')
    broker = Broker()
    broker.run()
    
def create_publishers():
    print('creating pub1 ')
    pub1 = Publisher('topic1',3)
    print('creating pub2 ')
    pub2 = Publisher('topic2',2)
    while True:
        time.sleep(1)
        reply = pub1.send('hello')
        print(reply)
        message = 'hello again'
        reply = pub2.send(message)
        print(reply)

def create_subscribers1():
    print('creating sub1 ')
    sub1 = Subscriber('topic1',3)
    while True:
        reply = sub1.run()
        print('subscriber 1 ' , reply)

def create_subscribers2():
    print('creating sub2 ')
    sub2 = Subscriber('topic2',3)
    print('subscribers started')
    while True:
        reply = sub2.run()
        print('subscriber 2 ' , reply)
        
if __name__ == "__main__":
    print('starting broker process')
    Process(target=start_broker).start()
    print('creating publishers process')
    Process(target=create_publishers).start()
    print('creating subscribers process')
    Process(target=create_subscribers1).start()
    print('starting subscribers')
    Process(target=create_subscribers2).start()
    print('process started')



