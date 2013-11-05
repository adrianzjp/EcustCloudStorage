# -*- coding: utf-8 -*-
'''
Created on 2013年9月22日

@author: adrian
'''

import os
import webob
from webob import Request
from webob import Response

import json

from api.api_map import ApiMapping

from metadata.data_model import DataLogic

from api.swift.swiftAPI import Connection
from api import settings

from services.backend.log.log import Log
import datetime

from emit_messages import EmitMeg

from meta_client import MetaClient

import re
import hashlib
    

class ContainerController():
    '''
    对于container的操作这里包含四个：
    PUT, GET, HEAD, DELETE
    
    这里使用metadata封装数据，实现了文件夹的嵌套功能。
    
    对于PUT操作，如果url中的container不存在，程序将建立一个文件夹，注意一个PUT操作一次最多只能建立一个文件夹。
    对于GET, HEAD, DELETE, PUT操作，如果url路径中的container不存在，则将报出404 Container NOT Found的错误
    
    metadata操作使用了基于rabbitmq的rpc操作
    api使用scloud标准api
    
    '''
    
    def __init__(self, global_conf):
        self.global_conf = global_conf
        self.token = ''
        self.userName = ''
        self.userKey = ''
        self.content = ''
        self.metadata_opr = DataLogic()
        pass
    
    def GET(self, environ,start_response):
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.meta_rpc = MetaClient()

        
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
        
        parent_id = 0
        
        flag = 1
        resheaders = []
        
#         这里我们将遍历url中的所有的container
        
        for i in xrange(c_len):
            c_name = containers[i]
            
            # get all the containers corresponding to such conditions    
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
            containers_get = self.meta_rpc.call(**kwargs)
            containers_dic = json.loads(containers_get)
            
            print c_len
            if len(containers_dic) != 0:
                parent_id = containers_dic[0].get('id','')
                storage_name = containers_dic[0].get('m_storage_name', '')

                if i == c_len-1:
                    
                    try:
            #             def get_auth(url, user, key, tenant_name=None):
                        print self.global_conf['AUTH_URL']
                        auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
                        
                        dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
                        url, token = ApiMapping().scloud_get_auth(**dic)
                        
                        dic = {"storage_url":url, 'token':token, 'container':storage_name,'headers':{}}
#                         ApiMapping().scloud_put_container(**dic)
#                         ApiMapping().scloud_delete_container(**dic)
                        headers, content = ApiMapping().scloud_get_container(**dic)
                        
                        self.content = str(content)
            
                        Log().info('GET_CONTAINER by '+self.userName+': '+self.domain+'/'+c_name)
                        
                        for value in headers:
                            x = (value,headers[value])
                            resheaders.append(x)
            #                 print value

                        break
                        
                    except Exception,e:
                        flag = 0
                        Log().error('PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
                        break
            else:
                print 'Containers not Found'
                flag = 0

        
        if flag:
            start_response("200 OK", resheaders)

#             return [str(contianers_in_account),]
        else:
            start_response("404 Container Not Found", [])
#             return ["you are not authenticated"]
        
        return self.content           

        
    def HEAD(self, environ,start_response):
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.meta_rpc = MetaClient()

        
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
        
        parent_id = 0
        
        flag = 1
        resheaders = []
        
#         这里我们将遍历url中的所有的container
        
        for i in xrange(c_len):
            c_name = containers[i]
            
            # get all the containers corresponding to such conditions    
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
            containers_get = self.meta_rpc.call(**kwargs)
            containers_dic = json.loads(containers_get)
            
            if len(containers_dic) != 0:
                parent_id = containers_dic[0].get('id','')
                storage_name = containers_dic[0].get('m_storage_name', '')

                if i == c_len-1:
                    try:
            #             def get_auth(url, user, key, tenant_name=None):
                        print self.global_conf['AUTH_URL']
                        auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
                        
                        dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
                        url, token = ApiMapping().scloud_get_auth(**dic)
                        
                        dic = {"storage_url":url, 'token':token, 'container':storage_name,'headers':{}}
#                         ApiMapping().scloud_put_container(**dic)
#                         ApiMapping().scloud_delete_container(**dic)
                        resbody = ApiMapping().scloud_head_container(**dic)

            
                        Log().info('GET_CONTAINER by '+self.userName+': '+self.domain+'/'+c_name)
                        
                        for value in resbody:
                            x = (value,resbody[value])
                            resheaders.append(x)
            #                 print value
                        print resheaders
                        break
                        
                    except Exception,e:
                        flag = 0
                        Log().error('PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
                        break
            else:
                print 'Containers not Found'
                flag = 0

        
        if flag:
            start_response("200 OK", resheaders)
#             return [str(contianers_in_account),]
        else:
            start_response("404 Container Not Found", [])
#             return ["you are not authenticated"]
        
        return self.content        
        

        
        
    def PUT(self, environ,start_response):
        '''
            the url curl   -i -H "X-Auth-Key: ADMIN"  -H "X-Auth-User: admin" 
             http://localhost:8080/scloud_container/domain/c1/c2/c3/c4   -X PUT
             
            this PUT method will only find the first not existing container then creat it.
            will Ignore the others containers which does not exist.
            
            and return the metadata of the new container which contains the metadata of the container
        
        '''
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.meta_rpc = MetaClient()
        
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
        
        parent_id = 0
        
        flag = 1
        resheaders = []
        for i in xrange(c_len):
            c_name = containers[i]
            print parent_id
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
            containers_get = self.meta_rpc.call(**kwargs)
            containers_dic = json.loads(containers_get)
            if len(containers_dic) == 0:
                print 'Container Not Found'
                try:
        #             def get_auth(url, user, key, tenant_name=None):
                    print self.global_conf['AUTH_URL']
                    auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
                    
                    dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
                    url, token = ApiMapping().scloud_get_auth(**dic)
                    
                    container_name_construct = self.userName+'_'+str(parent_id)+'_'+c_name+'_'+self.domain+'_'+'container_'+"".join(re.split('\W+', str(datetime.datetime.now())))
                    container_storagename = hashlib.md5(container_name_construct).hexdigest()  
                    dic = {"storage_url":url, 'token':token, 'container':container_storagename,'headers':{}}
                    ApiMapping().scloud_put_container(**dic)
        
        #             headers,body=  (Connection(authurl =auth_url, user = self.userName,\
        #                             key = self.userKey, tenant_name = req.headers['domain']).get_object(req.headers['container'], req.headers['object']))
                    
                    kwargs = {
                                'm_name' : c_name,
                                'm_storage_name' : container_storagename,
                                'm_domain_name' : self.domain,
                                'm_content_type' : 'container',
                                'm_status' : '1',   #'1' means available, '0' means not available
                                'm_uri' : container_storagename,
                                'm_hash' : '', #here we do not assign a hash name to the container
                                'm_size' : '2G',
                                'm_parent_id' : parent_id,
                                'created' : str(datetime.datetime.now()),
                                 
                                'metadata_opr':'add'#this is for the mq know what kind of opr it is...
                     
                    }      
                    
                    self.meta_rpc.call(**kwargs)
                    for item in kwargs.items():
                        resheaders.append(item)
                    
                    break
                    
                except Exception,e:
                    flag = 0
                    print e
                    Log().error('PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
                    pass
                print c_name
            else:
                print 'Containers exists'
                parent_id = containers_dic[0].get('id','')
                print c_name

        
        if flag:
            start_response("200 OK", resheaders)
#             return [str(contianers_in_account),]
        else:
            start_response("200 OK", [])
#             return ["you are not authenticated"]
        
        return self.content
        
        
    def DELETE(self, environ,start_response):
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.meta_rpc = MetaClient()

        
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
        
        parent_id = 0
        
        flag = 1
        resheaders = []
        
        for i in xrange(c_len):
            c_name = containers[i]
            
            # get all the containers corresponding to such conditions    
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
            containers_get = self.meta_rpc.call(**kwargs)
            containers_dic = json.loads(containers_get)
            
            if len(containers_dic) != 0:
                parent_id = containers_dic[0].get('id','')
                storage_name = containers_dic[0].get('m_storage_name', '')

                if i == c_len-1:
                    try:
            #             def get_auth(url, user, key, tenant_name=None):
                        print self.global_conf['AUTH_URL']
                        auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
                        
                        dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
                        url, token = ApiMapping().scloud_get_auth(**dic)
                        
                        dic = {"storage_url":url, 'token':token, 'container':storage_name,'headers':{}}
#                         ApiMapping().scloud_put_container(**dic)
                        ApiMapping().scloud_delete_container(**dic)

                        kwargs = {'id' : parent_id, 'metadata_opr':'delete'}
                        self.meta_rpc.call(**kwargs)
                        break
                        
                    except Exception,e:
                        flag = 0
                        Log().error('PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
                        break
            else:
                print 'Containers not Found'
                flag = 0

        
        if flag:
            start_response("200 OK", resheaders)
#             return [str(contianers_in_account),]
        else:
            start_response("404 Container Not Found", [])
#             return ["you are not authenticated"]
        
        return self.content        

    
    def __call__(self,environ,start_response):
        
        req = Request(environ)
        if req.method == 'GET':
            self.GET(environ, start_response)
        if req.method == "HEAD":
            self.HEAD(environ, start_response)
        if req.method == "PUT":
            self.PUT(environ, start_response)
        if req.method == "DELETE":
            self.DELETE(environ, start_response)
            
        return [self.content,]
        
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return ContainerController(global_conf)
    
    
    
    