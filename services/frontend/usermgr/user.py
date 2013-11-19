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
    

class User():
    def __init__(self, global_conf):
        self.global_conf = global_conf
        self.token = ''
        self.userName = ''
        self.userKey = ''
        pass
    
    
    def __call__(self,environ,start_response):
        
        req = Request(environ)
        res = Response()

        self.userName = ''
        self.userKey = ''
        self.token = ''
        print req.headers['token']
        
        
        
        for n in req.headers:
            if 'X-Auth-User' == n:
                self.userName = str(req.headers[n]).strip()
            if 'X-Auth-Key' == n:
                self.userKey = str(req.headers[n]).strip()
#         aus = Client(auth_url=settings.AUTH_URL,username='admin',password='ADMIN')
        try:
            
            auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
            name = self.userName
            passw = self.userKey
            
            
            url, self.token =  Connection(authurl =auth_url, user = self.userName, key = passw, tenant_name = 'admin')\
            .get_auth()
#             print conn.head_account()
#             print token
#             self.token = token
#             print self.token, self.userKey, self.userName
        except Exception,e:
            print e
            pass
        if self.token!='':
            start_response("200 OK",[("Content-type", "text/plain"),
                                     ("X-Storage-Url","https://storage.swiftdrive.com/v1/CF_xer7_343"),
                                     ("X-token", str(self.token))])
            return ["you are authenticated",]
        else:
            return ["you are not authenticated"]
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return User(global_conf)