
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"

i = 0
while i < 10:
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=message+str(i)+'....'*i,
                          properties=pika.BasicProperties(
                             delivery_mode = 2, # make message persistent
                          ))
    print " [x] Sent %r" % (message+str(i)+'....'*i,)
    i = i+1
    
connection.close()