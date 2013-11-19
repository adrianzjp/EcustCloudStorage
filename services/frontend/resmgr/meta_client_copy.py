# -*- coding: utf-8 -*-
'''
Created on 2013年11月4日

@author: adrian
'''
import pika
import uuid
import json



class MetaClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, **meg):
        self.response = None
        meta_json = json.dumps(meg, ensure_ascii=False)
        print meta_json
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key = 'meta_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=meta_json)
        while self.response is None:
            self.connection.process_data_events()
        print self.response

for i in xrange(5):
    meta_rpc = MetaClient()
    kwargs = {'id': '48', 'metadata_opr':'get'}
    
    print meta_rpc.call(**kwargs)

# print " [x] Requesting fib(30)"
# response = meta_rpc.call(30)
# print " [.] Got %r" % (response,)