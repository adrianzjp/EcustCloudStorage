# -*- coding: utf-8 -*-
'''
Created on 2013年9月22日

@author: adrian
'''

import os
import webob
from webob import Request
from webob import Response

from proxy.params import *

import json

from api.api_map import ApiMapping

from metadata.data_model import DataLogic
from metadata.domain_model import DomainLogic

from api.swift.swiftAPI import Connection
from api import settings

from services.backend.log.log import Log
import datetime


from rpc import Rpc

import re
import hashlib
    

class ContainerController():
    '''
    对于container的操作这里包含四个：
    PUT, GET, HEAD, DELETE, POST
    
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
        pass
    
    def GET(self, environ,start_response):
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.rpc = Rpc()

        
        containers = req.headers.get('container','')
        
        print containers
        
        c_len = len(containers)# the length of the container list
        
        #modified by adrian
        #use rabbit to diliver message
        kwargs = {'metadata_target':'domain', 'name':self.domain, 'metadata_opr':'get'}
        domains_get = self.rpc.call('meta_queue', **kwargs)
        domains_dic = json.loads(domains_get)
        
        parent_id = domains_dic[0].get('id', '')
        
        if parent_id == '':
            req.headers['http-flag'] = HTTPInternalServerError
            log_dic = {"log_flag":"error", "content":'can not get the domain ['+self.domain+"] id"}
            self.rpc.cast('logs', json.dumps(log_dic))             
#         parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
        
        flag = 1
        resheaders = []
        
#         这里我们将遍历url中的所有的container
        
        for i in xrange(c_len):
            c_name = containers[i]
            
            # get all the containers corresponding to such conditions    
            kwargs = {'metadata_target':'data', 'm_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id, 'm_content_type':'container'}
            containers_get = self.rpc.call('meta_queue', **kwargs)
            containers_dic = json.loads(containers_get)
            
#             print c_len
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
                        
                        '''
                        codes below to change the storage_name to logical name
                        '''
                        
                        for container in content:
                            kwargs = {'metadata_target':'data', 'm_storage_name':container.get('name'), 'metadata_opr':'get'}
                            containers_get = self.rpc.call('meta_queue', **kwargs)
                            containers_dic = json.loads(containers_get)
                            if len(containers_dic) != 0:
                                c_logic_name = containers_dic[0].get('m_name')
                                container['name'] = c_logic_name
                                
                        self.content = str(content)
                        log_dic = {"log_flag":"info", "content":'GET_CONTAINER by '+self.userName+': '+self.domain+'/'+c_name}
                        self.rpc.cast('logs', json.dumps(log_dic)) 
                        
                        for value in headers:
                            if value != 'content-length':
                                x = (value,headers[value])
                                resheaders.append(x)
            #                 print value

                        break
                        
                    except Exception,e:
                        flag = 0
                        log_dic = {"log_flag":"error", "content":'PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e)}
                        self.rpc.cast('logs', json.dumps(log_dic)) 
                        break
            else:
                print 'Containers not Found'
                flag = 0
            

        if flag:
            content_length = ('content-length', str(len(self.content)))
            resheaders.append(content_length)
            start_response("200 OK", resheaders)
#             return [str(contianers_in_account),]
        else:
            self.content = 'you are not authenticated'
            content_length = ('content-length', str(len(self.content)))
            resheaders.append(content_length)
            start_response("403 not authenticated", resheaders)
#             return ["you are not authenticated"]
        return self.content

        
    def HEAD(self, environ,start_response):
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.rpc = Rpc()

        
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
        
        
        #modified by adrian
        #use rabbit to diliver message
        kwargs = {'metadata_target':'domain', 'name':self.domain, 'metadata_opr':'get'}
        domains_get = self.rpc.call('meta_queue', **kwargs)
        domains_dic = json.loads(domains_get)
        
        parent_id = domains_dic[0].get('id', '')
        
        if parent_id == '':
            req.headers['http-flag'] = HTTPInternalServerError
            log_dic = {"log_flag":"error", "content":'can not get the domain ['+self.domain+"] id"}
            self.rpc.cast('logs', json.dumps(log_dic))           
#         parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
        
        flag = 1
        resheaders = []
        
#         这里我们将遍历url中的所有的container
        
        for i in xrange(c_len):
            c_name = containers[i]
            
            # get all the containers corresponding to such conditions    
            kwargs = {'metadata_target':'data', 'm_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id,  'm_content_type':'container'}
            containers_get = self.rpc.call('meta_queue', **kwargs)
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
                        log_dic = {"log_flag":"info", "content":'GET_CONTAINER by '+self.userName+': '+self.domain+'/'+c_name}
                        self.rpc.cast('logs', json.dumps(log_dic)) 
            
                        
                        for value in resbody:
                            x = (value,resbody[value])
                            resheaders.append(x)
            #                 print value
                        print resheaders
                        break
                        
                    except Exception,e:
                        flag = 0
                        log_dic = {"log_flag":"error", "content":'PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e)}
                        self.rpc.cast('logs', json.dumps(log_dic)) 
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
            
            and returns the metadata of the new container
        
        '''
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.rpc = Rpc()
        
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
        
        
        #modified by adrian
        #use rabbit to diliver message
        kwargs = {'metadata_target':'domain', 'name':self.domain, 'metadata_opr':'get'}
        domains_get = self.rpc.call('meta_queue', **kwargs)
        domains_dic = json.loads(domains_get)
        
        parent_id = domains_dic[0].get('id', '')
        
        if parent_id == '':
            req.headers['http-flag'] = HTTPInternalServerError
            log_dic = {"log_flag":"error", "content":'can not get the domain ['+self.domain+"] id"}
            self.rpc.cast('logs', json.dumps(log_dic))           
#         parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
        
        flag = 1
        resheaders = []
        for i in xrange(c_len):
            c_name = containers[i]
            print 'hello'
            kwargs = {'metadata_target':'data', 'm_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id, 'm_content_type':'container'}
            containers_get = self.rpc.call('meta_queue', **kwargs)
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
                                'metadata_target':'data',
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
                    
                    self.rpc.call('meta_queue', **kwargs)
                    for item in kwargs.items():
                        resheaders.append(item)
                    
                    break
                    
                except Exception,e:
                    flag = 0
                    print e
                    log_dic = {"log_flag":"error", "content":'PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e)}
                    self.rpc.cast('logs', json.dumps(log_dic))
                    pass
                print c_name
            else:
                print 'Containers exists'
                flag = 2
                parent_id = containers_dic[0].get('id','')
                print c_name

        
        if flag == 1:
            start_response("200 OK", resheaders)
#             return [str(contianers_in_account),]
        elif flag == 2:
            start_response("403 Containers already exists", resheaders)
            
        else:
            start_response("500 Error", [])
#             return ["you are not authenticated"]
        
        return self.content
        
        
    def DELETE(self, environ,start_response):
        
        '''
            we propose that if the container contains some objects, then delete operation
            is forbidden
        '''
        
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.rpc = Rpc()

        
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
        
        
        #modified by adrian
        #use rabbit to diliver message
        kwargs = {'metadata_target':'domain', 'name':self.domain, 'metadata_opr':'get'}
        domains_get = self.rpc.call('meta_queue', **kwargs)
        domains_dic = json.loads(domains_get)
        
        parent_id = domains_dic[0].get('id', '')
        
        if parent_id == '':
            req.headers['http-flag'] = HTTPInternalServerError
            log_dic = {"log_flag":"error", "content":'can not get the domain ['+self.domain+"] id"}
            self.rpc.cast('logs', json.dumps(log_dic))           
#         parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
        
        flag = 1
        resheaders = []
        
        for i in xrange(c_len):
            c_name = containers[i]
            
            # get all the containers corresponding to such conditions    
            kwargs = {'metadata_target':'data', 'm_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id,  'm_content_type':'container'}
            containers_get = self.rpc.call('meta_queue', **kwargs)
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

                        kwargs = {'metadata_target':'data', 'id' : parent_id, 'metadata_opr':'delete'}
                        self.rpc.call('meta_queue', **kwargs)
                        break
                        
                    except Exception,e:
                        flag = 0
                        log_dic = {"log_flag":"error", "content":'PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e)}
                        self.rpc.cast('logs', json.dumps(log_dic))
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

    
        
    def POST(self, environ,start_response):
        
        '''POST can be used to change container metadata
        like to change container name
        
        the curl request like below:
            
            curl   -i 
            -H "original-name:container_old" -H "current-name:container_new"  
            -H "X-Auth-Key: alex"  
            -H "X-Auth-User: alex"  
            http://localhost:8080/scloud_container/[domain-name]/[existing-container]
            -X POST
            
            :param container_old is  in [existing-container]
            :param container_new will replace as new container name
            
        '''
        
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        
        self.original_name = req.headers.get('original-name','')
        self.current_name = req.headers.get('current-name','')
        
        self.rpc = Rpc()

        containers = req.headers.get('container','')
        containers.append(self.original_name)

        c_len = len(containers)# the length of the container
        
        
        #modified by adrian
        #use rabbit to diliver message
        kwargs = {'metadata_target':'domain', 'name':self.domain, 'metadata_opr':'get'}
        domains_get = self.rpc.call('meta_queue', **kwargs)
        domains_dic = json.loads(domains_get)
        
        parent_id = domains_dic[0].get('id', '')
        
        if parent_id == '':
            req.headers['http-flag'] = HTTPInternalServerError
            log_dic = {"log_flag":"error", "content":'can not get the domain ['+self.domain+"] id"}
            self.rpc.cast('logs', json.dumps(log_dic))           
        #initialize the parent_id which is the id of domain
#         parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
        
        flag = 1
        resheaders = []
        
        if self.original_name == '':
            start_response("original name required", [])
            return self.content
#             flag = 0
        

        if self.current_name == '':
            start_response("current name required", [])
            return self.content
#             flag = 0
        
        for i in xrange(c_len):
            c_name = containers[i]
            
            # get all the containers corresponding to such conditions    
            kwargs = {'metadata_target':'data', 'm_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id,  'm_content_type':'container'}
            containers_get = self.rpc.call('meta_queue', **kwargs)
            containers_dic = json.loads(containers_get)
            
            if len(containers_dic) != 0:
                parent_id = containers_dic[0].get('id','')

                if i == c_len-1:
                    try:
                        kws = {'metadata_target':'data', 'm_name':self.current_name, 'metadata_opr':'get',  'm_content_type':'container'}
                        c_get = self.rpc.call('meta_queue', **kws)
                        c_dic = json.loads(c_get)
                        
                        if len(c_dic) == 0:
                            kwargs = {'metadata_target':'data', 'id':parent_id, 'm_name':self.current_name, 'metadata_opr':'update'}
                            self.rpc.call('meta_queue', **kwargs)
                        break
                        
                    except Exception,e:
                        flag = 0
                        log_dic = {"log_flag":"error", "content":'PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e)}
                        self.rpc.cast('logs', json.dumps(log_dic))
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
        if req.method == "POST":
            self.POST(environ, start_response)
            
        return [self.content,]
        
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return ContainerController(global_conf)
    
    
    
    