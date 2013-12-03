# -*- coding: utf-8 -*-
'''
Created on 2013年12月3日

@author: adrian
'''
import pika
import sys
import json
import httplib, urllib

class Worker(object):
    '''
    用户注册的service，在xml配置完成之后，要在此实现相应的on_request方法
    '''
    def __init__(self, host, exchange, exchange_type, routing_key, on_request_name):
        '''
        :param host: 用户配置的Rabbit Mq Server所在IP地址
        :param exchange: 用户配置的交换机名称
        :param exchange_type: 用户配置的交换机类型
        :param routing_key: 用户配置的路由key， 此key等同于queue的名称
        :param on_request_name: 用户配置的服务器接收响应的方法名称
        '''
        connection = pika.BlockingConnection(pika.ConnectionParameters(host = host or 'localhost'))
        channel = connection.channel()
        channel.queue_declare(queue = routing_key)
        channel.basic_qos(prefetch_count = 1)
        channel.basic_consume(on_request_name, queue = routing_key)
         
        print " [x] Awaiting RPC requests"
        channel.start_consuming()
        
    def url_go(self, domain_id, size, opr):
        #:param opr is GET or POST
        #:param domain_id is the id of domain
        #:param size is size of object file
    
        body = ''
    
        conn = httplib.HTTPConnection("localhost:8888")
        conn.request(opr, '/?id='+domain_id+'&size='+size, body, {})
        try:
            response = conn.getresponse()
            result = response.read()
            return result
        except Exception, e:
            print e
 
    def on_request(self, ch, method, props, body):
        
        mes_dic = json.loads(body)
        #获得操作指令   GET or POST
        opr = mes_dic.pop('opr')
        #获得文件大小
        size = mes_dic.pop('size')
        #获得域id
        domain_id = mes_dic.pop('id')
         
         
        response = self.url_go(domain_id, size, opr)
             
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)



#For Test
if __name__ == '__main__':
    worker = Worker()    