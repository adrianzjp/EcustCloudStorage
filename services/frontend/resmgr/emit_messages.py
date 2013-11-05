# -*- coding: utf-8 -*-
'''
Created on 2013年10月28日

@author: adrian
'''
import pika
import sys
import json
import datetime

class EmitMeg():
    def __init__(self):
        pass
    def emit_meg(self, routing_key, **meg):
        
        '''
        the message format should be like this:
            [opr]
        
        '''
        
        meg_json = json.dumps(meg, ensure_ascii=False)
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()
        
        channel.exchange_declare(exchange='direct_meg',
                                 type='direct')
        
        channel.basic_publish(exchange='direct_meg',
                              routing_key=routing_key,
                              body= meg_json)
        print " [x] Sent %r:%r" % (routing_key, meg)
        connection.close()
# emit_meg('metadata',**{})


if __name__ == '__main__':
    meg = EmitMeg()
    kwargs = {
                        'm_name' : 'self.container',
                        'm_storage_name' : 'haha',
                        'm_domain_name' : 'self.domain',
                        'm_content_type' : 'container',
                        'm_status' : '1',
                        'm_uri' : 'hello.zjp',
                        'm_hash' : '',
                        'm_size' : '2G',
                        'm_parent_id' : 0,
                        'created' : str(datetime.datetime.now()),
                        'metadata_opr':'add'}
    meg.emit_meg('metadata', **kwargs)
