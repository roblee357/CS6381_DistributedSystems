import publisher

# publisher.main

pub1 = publisher.Publisher('topic1',3)
reply = pub1.send('hello')
print(reply)

pub2 = publisher.Publisher('topic2',2)
message = 'hello again'
reply = pub2.send(message)
print(reply)