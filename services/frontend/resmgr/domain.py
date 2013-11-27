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

# from api.keystone.client import Client
# from api.keystone import *

from api.swift.swiftAPI import Connection
from api.api_map import ApiMapping

from api import settings

from meta_client import MetaClient


from services.backend.log.log import Log    

class DomainController():
    def __init__(self, global_conf):
        self.global_conf = global_conf
        self.token = ''
        self.userName = ''
        self.userKey = ''
        self.content = ''
        pass
    
    def GET(self, environ,start_response):
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.token = ''
        self.meta_rpc = MetaClient()


        flag = 1
        contianers_in_account = ''
        resheaders = []
        try:
#             def get_auth(url, user, key, tenant_name=None):
            print self.global_conf['AUTH_URL']
            auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
            
            dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
            url, token = ApiMapping().scloud_get_auth(**dic)
            dic = {"storage_url":url, 'token':token}
            resbody,contianers_in_account = ApiMapping().scloud_get_domain(**dic)
            
            print contianers_in_account
            
            '''
            codes below to change the storage_name to logical name
            '''
            
            for container in contianers_in_account:
                kwargs = {'m_storage_name':container.get('name'), 'metadata_opr':'get', 'm_content_type':'container'}
                containers_get = self.meta_rpc.call(**kwargs)
                containers_dic = json.loads(containers_get)
                if len(containers_dic) != 0:
                    c_logic_name = containers_dic[0].get('m_name')
                    container['name'] = c_logic_name
             
            Log().info('GET_DOMAIN by '+self.userName+': '+self.domain)

            
            for value in resbody:
                if value != 'content-length':
                    x = (value,resbody[value])
                    resheaders.append(x)
            
#                 print value
#             print token
#             self.token = token
#             print self.token, self.userKey, self.userName
        except Exception,e:
            flag = 0
            Log().error('GET_DOMAIN by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+' '+str(e))
            print e
            
        
        if flag:
            self.content = repr(contianers_in_account)
            content_length = ('content-length', str(len(self.content)))
            resheaders.append(content_length)
            start_response("200 OK", resheaders)
#             return [str(contianers_in_account),]
        else:
            self.content = 'you are not authenticated'
            content_length = ('content-length', str(len(self.content)))
            resheaders.append(content_length)
            start_response("403 not authenticated", resheaders)
        
#         return self.content
        
    def HEAD(self, environ,start_response):
        req = Request(environ)
        res = Response()

        self.content = ''
        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')

        flag = 1
        resheaders = []
        try:
#             def get_auth(url, user, key, tenant_name=None):
            print self.global_conf['AUTH_URL']
            auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
            
#             first we here get url and token
            dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
            url, token = ApiMapping().scloud_get_auth(**dic)
            
#             we send the url and token to the api params
            dic = {"storage_url":url, 'token':token}
            resbody= ApiMapping().scloud_head_domain(**dic)
            
#             resbody=  (Connection(authurl =auth_url, user = self.userName,\
#                             key = self.userKey, tenant_name = req.headers['domain']).head_account())
            
            Log().info('HEAD_DOMAIN by '+self.userName+': '+self.domain)

            for value in resbody:
                x = (value,resbody[value])
                resheaders.append(x)
#                 print value
            print resheaders
#             print token
#             self.token = token
#             print self.token, self.userKey, self.userName
        except Exception,e:
            flag = 0
            Log().error('HEAD_DOMAIN by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+' '+str(e))
            print e
            pass
        if flag:
            start_response("200 OK", resheaders)
#             return [str(contianers_in_account),]
        else:
            start_response("200 OK", [])
#             return ["you are not authenticated"]
        
        return self.content
        
    
    
    def __call__(self,environ,start_response):
        
        req = Request(environ)
        if req.method == 'GET':
            self.GET(environ, start_response)
        if req.method == "HEAD":
            self.HEAD(environ, start_response)
            
        return [self.content]
        
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return DomainController(global_conf)
    
    
    
    