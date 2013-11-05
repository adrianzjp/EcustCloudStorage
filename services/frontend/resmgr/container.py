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
from api import settings

    

class AccountController():
    def __init__(self, global_conf):
        self.global_conf = global_conf
        self.token = ''
        self.userName = ''
        self.userKey = ''
        pass
    def GET(self, req):
        
        
        
        pass
    
    
    
    def __call__(self,environ,start_response):
        
        req = Request(environ)
        res = Response()

        self.userName = 'x'
        self.userKey = 'x'
        self.token = ''
        
        for n in req.headers:
            if 'X-Auth-User' == n:
                self.userName = req.headers[n]
            if 'X-Auth-Key' == n:
                self.userKey = req.headers[n]
#         aus = Client(auth_url=settings.AUTH_URL,username='admin',password='ADMIN')

        flag = 1
        contianers_in_account = ''
        resheaders = []
        try:
#             def get_auth(url, user, key, tenant_name=None):
            print self.global_conf['AUTH_URL']
            auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
            resbody,contianers_in_account=  (Connection(authurl =auth_url, user = self.userName,\
                            key = self.userKey, tenant_name = 'admin').get_account())
            
            
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
            print e
            pass
        if flag:
            start_response("200 OK", resheaders)
            return [str(contianers_in_account),]
        else:
            return ["you are not authenticated"]
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return AccountController(global_conf)
    
    
    
    