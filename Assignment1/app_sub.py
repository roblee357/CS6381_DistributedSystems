from subscriber import *

# publisher.main

sub1 = Subscriber('topic2',3)
while True:
    reply = sub1.run()
    print(reply)
