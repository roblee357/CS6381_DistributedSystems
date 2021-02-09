import sys, zmq, json

class Subscriber():
    def __init__(self, topic,sub_id):
        with open('config.json','r') as fin:
            config = json.load(fin)
        self.use_broker = config['use_broker']
        con_str = "tcp://" + config['ip'] + ":" + config['pub_port']
        self.topic = topic
        self.sub_id = sub_id
        # print('Creating the object')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.topicfilter = str.encode(self.topic)
        

        if self.use_broker:

            with open('config.json','r') as fin:
                config = json.load(fin)
            #  Socket to talk to server
            # print("Connecting to broker...")
            
            self.con_str = "tcp://" + config['ip'] + ":" + config['sub_port']
            # print(self.con_str)
            self.socket.connect(self.con_str)
            self.socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)
            
            
        else:
        #    #  Socket to talk to server
        #     self.context = zmq.Context()

        #     # Since we are the subscriber, we use the SUB type of the socket
        #     socket = context.socket(zmq.SUB)

            # Here we assume publisher runs locally unless we
            # send a command line arg like 10.0.0.2
            srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
            connect_str = "tcp://" + srv_addr + ":5556"

            print("Collecting updates from weather server proxy at: {}".format(connect_str))
            self.socket.connect(connect_str)
            print(self.topicfilter)
            # # Subscribe to zipcode, default is NYC, 10001
            zip_filter = sys.argv[2] if len(sys.argv) > 2 else "10001"

            # # Python 2 - ascii bytes to unicode str
            # if isinstance(zip_filter, bytes):
            #     zip_filter = zip_filter.decode('ascii')

            # any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
            # system what it is interested in
            self.socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)
            # self.socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)

            # Process 5 updates
            total_temp = 0
            # for update_nbr in range(5):
            while True:
                string = self.socket.recv_string()
                print(string)
                # zipcode, temperature, relhumidity = string.split()
                # total_temp += int(temperature)

            print("Average temperature for zipcode '%s' was %dF" % (
                zip_filter, total_temp / (update_nbr+1))
            ) 

    def run(self):
        print('sub_id',self.sub_id,'subscribed to:' ,self.topic,'on', self.con_str)
        while True:
            string = self.socket.recv()
            if len(string)>0:
                return string
            # print(string)

# main
def main():
    sub1 = Subscriber('topic2',1)
    string = sub1.run()
    while True:
        reply = sub1.run()
        print(reply)

#----------------------------------------------
if __name__ == '__main__':
    main ()