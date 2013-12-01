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

from rpc import Rpc
from metadata.domain_model import DomainLogic


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
        self.rpc = Rpc()
        containers_object = req.headers.get('container','')
        containers_object.append(str(self.object))
        print containers_object
        c_len = len(containers_object)# the length of the container
         
        parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
        
        resheaders = []
        info = '200 OK'
        
        for i in xrange(c_len):
            c_name = containers_object[i]
            print parent_id
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
            containers_object_get = self.rpc.call('meta_queue', **kwargs)
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
                log_dic = {"log_flag":"info", "content":'GET_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object}
                self.rpc.cast('logs', json.dumps(log_dic))
                 
                for value in headers:
                    x = (value,headers[value])
                    resheaders.append(x)
                 
            except Exception,e:
                info = '404 Object Not Found'
                log_dic = {"log_flag":"error", "content":'GET_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+self.container+'/'+req.headers['object']+' '+str(e)}
                self.rpc.cast('logs', json.dumps(log_dic))
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
        self.rpc = Rpc()
        containers_object = req.headers.get('container','')
        containers_object.append(str(self.object))
        print containers_object
        c_len = len(containers_object)# the length of the container
         
        parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
         
        resheaders = []
        info = '200 OK'
        
        for i in xrange(c_len):
            c_name = containers_object[i]
            print parent_id
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
            containers_object_get = self.rpc.call('meta_queue', **kwargs)
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
                log_dic = {"log_flag":"info", "content":'HEAD_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object}
                self.rpc.cast('logs', json.dumps(log_dic))
                
                
#                 here is something that will be excuted after
#                 这里的response不支持content-length，后面需要解决这个问题！
                
                for item in headers.items():
                    if item[0]!= 'content-length':
                        resheaders.append(item)
                        
                    
                print resheaders
     
                 
            except Exception,e:
                info = '404 Object Not Found'
                print e
                log_dic = {"log_flag":"error", "content":'HEAD_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+self.container+'/'+req.headers['object']+' '+str(e)}
                self.rpc.cast('logs', json.dumps(log_dic))
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
        self.rpc = Rpc()
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
         
        parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
         
        resheaders = []
        info = '200 OK'
        
        for i in xrange(c_len):
            c_name = containers[i]
            print parent_id
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id, 'm_content_type':'container'}
            containers_get = self.rpc.call('meta_queue', **kwargs)
            containers_dic = json.loads(containers_get)
            
            #get the container name
            
            if len(containers_dic) == 0:
                info = '404 Container Not Found'
                break
            else:
                self.container = containers_dic[0].get('m_storage_name', '')
                parent_id = containers_dic[0].get('id','')
                
        if info == '200 OK':
            kwargs = {'m_name':self.object, 'metadata_opr':'get', 'm_parent_id':parent_id, 'm_content_type':'object'}
            object_get = self.rpc.call('meta_queue', **kwargs)
            object_dic = json.loads(object_get)
            
            #get the object name
            
            if len(object_dic) > 0:
                info = '404 Object already exists'
                
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
                    
                self.rpc.call('meta_queue', **kwargs)
                
                for item in kwargs.items():
                    resheaders.append(item)
                log_dic = {"log_flag":"info", "content":'PUT_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object}
                self.rpc.cast('logs', json.dumps(log_dic))
                 
            except Exception,e:
                info = '500 Internal Error'
                print e
                log_dic = {"log_flag":"error", "content":'PUT_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+self.container+'/'+req.headers['object']+' '+str(e)}
                self.rpc.cast('logs', json.dumps(log_dic))
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
        self.rpc = Rpc()
        containers_object = req.headers.get('container','')
        containers_object.append(str(self.object))
        print containers_object
        c_len = len(containers_object)# the length of the container
         
        parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
         
        resheaders = []
        info = '200 OK'
        
        for i in xrange(c_len):
            c_name = containers_object[i]
            print parent_id
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
            containers_object_get = self.rpc.call('meta_queue', **kwargs)
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
                    
                self.rpc.call('meta_queue', **kwargs)
                
                log_dic = {"log_flag":"info", "content":'DELETE_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object}
                self.rpc.cast('logs', json.dumps(log_dic))
                 
            except Exception,e:
                info = '404 Object Not Found'
                print e
                log_dic = {"log_flag":"error", "content":'DELETE_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+self.container+'/'+req.headers['object']+' '+str(e)}
                self.rpc.cast('logs', json.dumps(log_dic))
                import sys
                print sys.exc_info()
         
        start_response(info, resheaders)
         
        return self.content
    
    def POST(self, environ,start_response):
        
        '''POST can be used to change object metadata
        like to change object name
        
        the curl request like below:
            
            curl   -i -H "original-name:love.html" -H "current-name:love_new.html"  
            -H "X-Auth-Key: alex"  -H "X-Auth-User: alex"  
            http://localhost:8080/scloud_object/alexhello/haha/love.html
             -X POST
            
            object_old is an existing container in haha
        '''
        
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        
        self.original_name = req.headers.get('object','')
        self.current_name = req.headers.get('current-name','')
        
        self.rpc = Rpc()

        containers = req.headers.get('container','')
#         containers.append(self.original_name)#here object added to the container lists

        c_len = len(containers)# the length of the container
        
        #initialize the parent_id which is the id of domain
        parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
        
        flag = 1
        resheaders = []
        
        if self.current_name == '':
            start_response("current name required", [])
            return self.content
#             flag = 0
        
        print containers
        
        for i in xrange(c_len):
            c_name = containers[i]
            
            # get all the containers corresponding to such conditions    
            kwargs = {'m_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id,  'm_content_type':'container'}
            containers_get = self.rpc.call('meta_queue', **kwargs)
            containers_dic = json.loads(containers_get)
            
            if len(containers_dic) != 0:
                parent_id = containers_dic[0].get('id','')
                if i == c_len-1:
                    try:
                        kws = {'m_name':self.original_name, 'm_parent_id':parent_id, 'metadata_opr':'get',  'm_content_type':'object'}
                        o_get = self.rpc.call('meta_queue', **kws)
                        o_dic = json.loads(o_get)
                        
                        object_id = o_dic[0].get('id','')
                        print object_id
                        if len(o_dic) != 0:
                            kws = {'m_name':self.current_name, 'm_parent_id':parent_id, 'metadata_opr':'get',  'm_content_type':'object'}
                            o_get = self.rpc.call('meta_queue', **kws)
                            o_dic = json.loads(o_get)
                            
                            if len(o_dic) == 0:
                                kwargs = {'id':object_id, 'm_name':self.current_name, 'metadata_opr':'update'}
                                self.rpc.call('meta_queue', **kwargs)
                        break
                        
                    except Exception,e:
                        
                        flag = 0
                        log_dic = {"log_flag":"error", "content":'PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e)}
                        self.rpc.cast('logs', json.dumps(log_dic))
                        break
            else:
                print 'Containers or Objects not Found'
                flag = 0

        
        if flag:
            start_response("200 OK", resheaders)
#             return [str(contianers_in_account),]
        else:
            start_response("404 Container or Object Not Found", [])
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
        return ObjectController(global_conf)
    
    
    
    