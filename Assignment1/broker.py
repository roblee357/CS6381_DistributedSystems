import time, sys, random
import zmq


class Broker:

    def __init__(self):
        # Request - Reply socket for publishers
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.REP)
        self.pub_socket.bind("tcp://*:5555")
        # Publish - Subscribe socket for subscribers
        self.port = "5556"
        if len(sys.argv) > 1:
            port =  sys.argv[1]
            int(port)
        #context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.PUB)
        self.sub_socket.bind("tcp://*:%s" % self.port)
        # Dictionary for holding subcriber and publisher information
        self.registry = {'PUB':[],'SUB':[]}

    def run(self):
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

def main():
    broker = Broker()
    broker.run()

#----------------------------------------------
if __name__ == '__main__':
    main ()