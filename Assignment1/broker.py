import time, sys, random, json
import zmq

class Broker:

    def __init__(self):
        with open('config.json','r') as fin:
            config = json.load(fin)
        self.use_broker = config['use_broker']
        if self.use_broker:
            # Request - Reply socket for publishers
            self.context = zmq.Context()
            self.pub_socket = self.context.socket(zmq.REP)
            self.pub_socket.bind("tcp://*:5555")
            # Publish - Subscribe socket for subscribers
            self.port = "5556"
            self.sub_socket = self.context.socket(zmq.PUB)
            self.sub_socket.bind("tcp://*:%s" % self.port)
            # Dictionary for holding subcriber and publisher information
            self.registry = {'PUB':[],'SUB':[]}
        else:
            # Get the context
            context = zmq.Context()

            # This is a proxy. We create the XSUB and XPUB endpoints
            print ("This is proxy: creating xsub and xpubsockets")
            xsubsocket = context.socket(zmq.XSUB)
            xsubsocket.bind("tcp://*:5555")

            xpubsocket = context.socket (zmq.XPUB)
            xpubsocket.setsockopt(zmq.XPUB_VERBOSE, 1)
            xpubsocket.bind ("tcp://*:5556")

            # This proxy is needed to connect the two sockets.
            # But what this means is that we cannot do anything here.
            # We are just relaying things internally.
            # This blocks
            zmq.proxy (xsubsocket, xpubsocket)

    def run(self):
        with open('config.json','r') as fin:
            config = json.load(fin)
        self.use_broker = config['use_broker']
        if self.use_broker:
            while True:
                #  Wait for next request from client
                self.message = self.pub_socket.recv()
                # print("Received request: %s" % message)
                self.decoded_message = self.message.decode("utf-8")
                print(self.decoded_message)
                if '_:_' in self.decoded_message:
                    self.deliminated_message = self.decoded_message.split('_:_')
                    self.app_type = self.deliminated_message[0]
                    self.ID = self.deliminated_message[1]
                    self.topic = self.deliminated_message[2]
                    self.message = self.deliminated_message[3]
                    print(self.app_type,self.topic,self.ID,self.message)
                
                    self.x = set(self.registry[self.app_type])
                    # print('x',x,'registry[app_type]',registry[app_type])
                    self.x.add(self.ID + ':' + self.topic)
                    self.registry[self.app_type] = self.x
                    print('registry',self.registry)

                    self.messagedata = self.message #random.randrange(1,215) - 80
                    print("%s %s" % (self.topic, self.messagedata))
                    self.bmessage = str.encode(str(self.topic) + ' ' + str(self.messagedata))
                    self.sub_socket.send(self.bmessage)
                    
                    self.pub_socket.send(b"Published " + self.bmessage)
                else:
                    self.pub_socket.send(b"Published " + self.message)

                time.sleep(.01)
        else:
            pass

def main():
    broker = Broker()
    broker.run()

#----------------------------------------------
if __name__ == '__main__':
    main ()