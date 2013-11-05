# -*- coding: utf-8 -*-
'''
Created on 2013年10月28日

@author: adrian
'''
import pika
import sys
import json

# to add the sys path in order python command in terminal can work 

# for mac
sys.path.append('/Users/adrian/Dropbox/workspace/EcustCloudStorage')

#for windows
# sys.path.append('C:\Users\jipingzh\Dropbox\workspace\EcustCloudStorage')



from metadata.data_model import DataLogic



connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_meg',
                         type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='direct_meg',
                       queue=queue_name,
                       routing_key='api')



def callback(ch, method, properties, body):
    mes_dic = json.loads(body)
#     print mes_dic
    opr = mes_dic.pop('metadata_opr')
    
    if 'add' == opr:
        DataLogic().add_data(**mes_dic)
        print mes_dic
    #     delete a data by id
    if 'delete' == opr:
        DataLogic().delete_data_by_id(**mes_dic)
    #     update data by id   
    if 'update' == opr:
        DataLogic().update_data_by_id(**mes_dic)
    # #     get data by conditions
    if 'get' == opr:
        DataLogic().get_by_kwargs(**mes_dic)
        
        
    
#     print " [x] %r:%r" % (method.routing_key, body,)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()