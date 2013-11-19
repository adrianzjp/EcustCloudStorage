# -*- coding: utf-8 -*-
'''
Created on 2013年9月22日

@author: adrian
'''

import os
import webob
from webob import Request
from webob import Response

# from api.keystone.client import Client
# from api.keystone import *

from api.swift.swiftAPI import Connection
from api.api_map import ApiMapping

from api import settings

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
            
#             resbody,contianers_in_account=  (Connection(authurl =auth_url, user = self.userName,\
#                             key = self.userKey, tenant_name = req.headers['domain']).get_account())
            
            Log().info('GET_DOMAIN by '+self.userName+': '+self.domain)

            
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
            Log().error('GET_DOMAIN by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+' '+str(e))
            print e
            pass
        if flag:
            start_response("200 OK", resheaders)
            self.content = str(contianers_in_account)
#             return [str(contianers_in_account),]
        else:
            self.content = 'you are not authenticated'
#             return ["you are not authenticated"]
        
        return self.content
        
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
            
        return [self.content,]
#         req = Request(environ)
#         res = Response()
#  
#         self.userName = 'x'
#         self.userKey = 'x'
#         self.token = ''
#          
#         for n in req.headers:
#             if 'X-Auth-User' == n:
#                 self.userName = req.headers[n]
#             if 'X-Auth-Key' == n:
#                 self.userKey = req.headers[n]
# #         aus = Client(auth_url=settings.AUTH_URL,username='admin',password='ADMIN')
#  
#         flag = 1
#         contianers_in_account = ''
#         resheaders = []
#         try:
# #             def get_auth(url, user, key, tenant_name=None):
#             print self.global_conf['AUTH_URL']
#             auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
#             resbody,contianers_in_account=  (Connection(authurl =auth_url, user = self.userName,\
#                             key = self.userKey, tenant_name = 'admin').get_account())
#              
#              
#             for value in resbody:
#                 x = (value,resbody[value])
#                 resheaders.append(x)
# #                 print value
# #             resheaders.append(('token',str(req.headers['token'])))
#             print resheaders
# #             print token
# #             self.token = token
# #             print self.token, self.userKey, self.userName
#         except Exception,e:
#             flag = 0
#             print e
#             pass
#         if flag:
# #             start_response("200 OK", resheaders)
#             return [str(contianers_in_account),]
#         else:
#             return ["you are not authenticated"]
        
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return DomainController(global_conf)
    
    
    
    