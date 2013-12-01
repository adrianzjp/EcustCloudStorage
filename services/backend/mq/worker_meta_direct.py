# -*- coding: utf-8 -*-
'''
Created on 2013年10月28日

@author: adrian
'''
import pika
import sys
import json

'''codes added to run in command'''
# for mac
sys.path.append('/Users/adrian/Dropbox/workspace/EcustCloudStorage')
#for windows
# sys.path.append('C:\Users\jipingzh\Dropbox\workspace\EcustCloudStorage')



from metadata.data_model import DataLogic

# to add the sys path in order python command in terminal can work 



connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='meta_queue')



def on_request(ch, method, props, body):
    mes_dic = json.loads(body)
    opr = mes_dic.pop('metadata_opr')
    
    if 'add' == opr:
        response = DataLogic().add_data(**mes_dic)
    #     delete a data by id
    if 'delete' == opr:
        response = DataLogic().delete_data_by_id(**mes_dic)
    #     update data by id   
    if 'update' == opr:
        response = DataLogic().update_data_by_id(**mes_dic)
    #     get data by conditions
    if 'get' == opr:
        response = DataLogic().get_by_kwargs(**mes_dic)
        
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='meta_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()




