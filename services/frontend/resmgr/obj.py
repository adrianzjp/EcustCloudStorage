# -*- coding: utf-8 -*-
'''
Created on 2013年9月22日

@author: adrian
'''

import os
import webob
from webob import Request
from webob import Response
from services.backend.log.log import Log
import json
from api.api_map import ApiMapping

from meta_client import MetaClient
import datetime
import hashlib
import re

    

class ObjectController():
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
        self.object = req.headers.get('object', '')
        self.meta_rpc = MetaClient()
        containers_object = req.headers.get('container','')
        containers_object.append(str(self.object))
        print containers_object
        c_len = len(containers_object)# the length of the container
         
        parent_id = 0
         
        resheaders = []
        info = '200 OK'
        
        for i in xrange(c_len):
            c_name = containers_object[i]
            print parent_id
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
            containers_object_get = self.meta_rpc.call(**kwargs)
            containers_object_dic = json.loads(containers_object_get)
            
            #get the container name
            
            if len(containers_object_dic) == 0:
                if i == c_len-1:
                    info = '404 Object Not Found'
                else:
                    info = '404 Container Not Found'
                break
            else:
                if i == c_len-1:
                    self.object = containers_object_dic[0].get('m_storage_name', '')
                else:
                    self.container = containers_object_dic[0].get('m_storage_name', '')
                    
                parent_id = containers_object_dic[0].get('id','')
                
        if info == '200 OK':
            try:
                auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
                
                dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
                url, token = ApiMapping().scloud_get_auth(**dic)
                 
                dic = {"storage_url":url, 'token':token, 'container':self.container,'headers':{}, \
                       'object':self.object,}
                
                headers, body = ApiMapping().scloud_get_object(**dic)
                
                self.content = str(body)
             
                Log().info('HEAD_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object)
                 
                for value in headers:
                    x = (value,headers[value])
                    resheaders.append(x)
    #                 print value
     
                Log().info('HEAD_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object)
                 
            except Exception,e:
                info = '404 Object Not Found'
                print e
                Log().error('HEAD_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+self.container+'/'+req.headers['object']+' '+str(e))
                import sys
                print sys.exc_info()
         
        start_response(info, resheaders)
         
        return self.content
        
        
    def HEAD(self, environ,start_response):
        
        self.content = ''

        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.object = req.headers.get('object', '')
        self.meta_rpc = MetaClient()
        containers_object = req.headers.get('container','')
        containers_object.append(str(self.object))
        print containers_object
        c_len = len(containers_object)# the length of the container
         
        parent_id = 0
         
        resheaders = []
        info = '200 OK'
        
        for i in xrange(c_len):
            c_name = containers_object[i]
            print parent_id
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
            containers_object_get = self.meta_rpc.call(**kwargs)
            containers_object_dic = json.loads(containers_object_get)
            
            #get the container name
            
            if len(containers_object_dic) == 0:
                if i == c_len-1:
                    info = '404 Object Not Found'
                else:
                    info = '404 Container Not Found'
                break
            else:
                if i == c_len-1:
                    self.object = containers_object_dic[0].get('m_storage_name', '')
                else:
                    self.container = containers_object_dic[0].get('m_storage_name', '')
                    
                parent_id = containers_object_dic[0].get('id','')
                
        if info == '200 OK':
            try:
                auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
                
                dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
                url, token = ApiMapping().scloud_get_auth(**dic)
                 
                dic = {"storage_url":url, 'token':token, 'container':self.container,'headers':{}, \
                       'object':self.object,}
                
                headers = ApiMapping().scloud_head_object(**dic)
 
#             headers,body=  (Connection(authurl =auth_url, user = self.userName,\
#                             key = self.userKey, tenant_name = req.headers['domain']).get_object(req.headers['container'], req.headers['object']))
             
                Log().info('HEAD_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object)
                
                
#                 here is something that will be excuted after
#                 这里的response不支持content-length，后面需要解决这个问题！
                
                for item in headers.items():
                    if item[0]!= 'content-length':
                        resheaders.append(item)
                        
                    
                print resheaders
     
                Log().info('HEAD_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object)
                 
            except Exception,e:
                info = '404 Object Not Found'
                print e
                Log().error('HEAD_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+self.container+'/'+req.headers['object']+' '+str(e))
                import sys
                print sys.exc_info()
         
        start_response(info, [ ('accept-ranges', 'bytes'), ('last-modified', 'Mon, 04 Nov 2013 14:42:02 GMT'), ('etag', 'd7d1c51fb2ea6a8d59bd3922f33bf7a7'), ('x-trans-id', 'tx8fadb8db0ea9465c83a0fdb00fa7fb58'), ('date', 'Mon, 04 Nov 2013 14:43:24 GMT'), ('content-type', 'application/octet-stream')])
         
        return self.content
        

        
    def PUT(self, environ,start_response):
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.object = req.headers.get('object', '')
        self.meta_rpc = MetaClient()
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
         
        parent_id = 0
         
        resheaders = []
        info = '200 OK'
        
        for i in xrange(c_len):
            c_name = containers[i]
            print parent_id
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
            containers_get = self.meta_rpc.call(**kwargs)
            containers_dic = json.loads(containers_get)
            
            #get the container name
            
            if len(containers_dic) == 0:
                info = '404 Container Not Found'
                break
            else:
                self.container = containers_dic[0].get('m_storage_name', '')
                parent_id = containers_dic[0].get('id','')
                
        if info == '200 OK':
            try:
                auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
                 
                sfile = req.body_file
                 
                dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
                url, token = ApiMapping().scloud_get_auth(**dic)
                
                object_name_construct = self.userName+'_'+str(parent_id)+'_'+self.object+'_'+self.domain+'_'+'object_'+"".join(re.split('\W+', str(datetime.datetime.now())))
                object_storagename = hashlib.md5(object_name_construct).hexdigest()  
                 
                dic = {"storage_url":url, 'token':token, 'container':self.container,'headers':{}, \
                       'object':object_storagename, 'contents':sfile}
                object_hash = ApiMapping().scloud_put_object(**dic)
                
                kwargs = {
                                'm_name' : self.object,
                                'm_storage_name' : object_storagename,
                                'm_domain_name' : self.domain,
                                'm_content_type' : 'object',
                                'm_status' : '1',   #'1' means available, '0' means not available
                                'm_uri' : object_storagename,
                                'm_hash' : object_hash ,
                                'm_size' : '2G',
                                'm_parent_id' : parent_id,
                                'created' : str(datetime.datetime.now()),
                                 
                                'metadata_opr':'add'#this is for the mq know what kind of opr it is...
                     
                    }      
                    
                self.meta_rpc.call(**kwargs)
                
                for item in kwargs.items():
                    resheaders.append(item)
     
                Log().info('PUT_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object)
                 
            except Exception,e:
                info = '500 Internal Error'
                print e
                Log().error('PUT_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+self.container+'/'+req.headers['object']+' '+str(e))
                import sys
                print sys.exc_info()
         
        start_response(info, resheaders)
         
        return self.content
        
        
    def DELETE(self, environ,start_response):
        self.content = ''
        
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.object = req.headers.get('object', '')
        self.meta_rpc = MetaClient()
        containers_object = req.headers.get('container','')
        containers_object.append(str(self.object))
        print containers_object
        c_len = len(containers_object)# the length of the container
         
        parent_id = 0
         
        resheaders = []
        info = '200 OK'
        
        for i in xrange(c_len):
            c_name = containers_object[i]
            print parent_id
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
            containers_object_get = self.meta_rpc.call(**kwargs)
            containers_object_dic = json.loads(containers_object_get)
            
            #get the container name
            
            if len(containers_object_dic) == 0:
                if i == c_len-1:
                    info = '404 Object Not Found'
                else:
                    info = '404 Container Not Found'
                break
            else:
                if i == c_len-1:
                    self.object = containers_object_dic[0].get('m_storage_name', '')
                else:
                    self.container = containers_object_dic[0].get('m_storage_name', '')
                    
                parent_id = containers_object_dic[0].get('id','')
                
        if info == '200 OK':
            try:
                auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
                
                dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
                url, token = ApiMapping().scloud_get_auth(**dic)
                 
                dic = {"storage_url":url, 'token':token, 'container':self.container,'headers':{}, \
                       'object':self.object,}
                
                ApiMapping().scloud_delete_object(**dic)
                
                kwargs = {
                            'id': parent_id,
                            'metadata_opr':'delete'#this is for the mq know what kind of opr it is...
                     
                    }      
                    
                self.meta_rpc.call(**kwargs)
                
             
                Log().info('DELETE_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object)
                 
            except Exception,e:
                info = '404 Object Not Found'
                print e
                Log().error('DELETE_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+self.container+'/'+req.headers['object']+' '+str(e))
                import sys
                print sys.exc_info()
         
        start_response(info, resheaders)
         
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
        return ObjectController(global_conf)
    
    
    
    