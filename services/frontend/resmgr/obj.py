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
<<<<<<< HEAD
    def GET(self, req):
=======
    
    def GET(self, environ,start_response):
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
            headers,body=  (Connection(authurl =auth_url, user = self.userName,\
                            key = self.userKey, tenant_name = req.headers['domain']).get_object(req.headers['container'], req.headers['object']))
            
            
            for value in headers:
                x = (value,headers[value])
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
            self.content = str(body)
#             return [str(contianers_in_account),]
        else:
            start_response("404 NoSuchFile", [])
            self.content = ''
#             return ["you are not authenticated"]
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
>>>>>>> parent of 32f7b0e... 2013-11-05
        
        return self.content
        
<<<<<<< HEAD
        
        pass
    
    
    
    def __call__(self,environ,start_response):
        
=======
=======
        
        return self.content
        
>>>>>>> parent of 32f7b0e... 2013-11-05
<<<<<<< HEAD
=======
        
        return self.content
        
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
    def HEAD(self, environ,start_response):
        req = Request(environ)
        res = Response()

        self.userName = 'x'
        self.userKey = 'x'
        self.token = ''
        self.content = ''
        for n in req.headers:
            if 'X-Auth-User' == n:
                self.userName = req.headers[n]
            if 'X-Auth-Key' == n:
                self.userKey = req.headers[n]
#         aus = Client(auth_url=settings.AUTH_URL,username='admin',password='ADMIN')

        flag = 1
        resheaders = []
        try:
#             def get_auth(url, user, key, tenant_name=None):
            print self.global_conf['AUTH_URL']
            auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
            headers=  (Connection(authurl =auth_url, user = self.userName,\
                            key = self.userKey, tenant_name = req.headers['domain']).head_object(req.headers['container'], req.headers['object']))
            
            
            for value in headers:
                x = (value,headers[value])
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
#             return [str(contianers_in_account),]
        else:
            start_response("200 OK", [])
#             return ["you are not authenticated"]
        
        return self.content
        
        
    def PUT(self, environ,start_response):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
>>>>>>> parent of 32f7b0e... 2013-11-05
        req = Request(environ)
        res = Response()

        self.userName = 'x'
        self.userKey = 'x'
        self.token = ''
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
        
=======
        self.content = ''
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
        self.content = ''
>>>>>>> parent of 32f7b0e... 2013-11-05
<<<<<<< HEAD
=======
        self.content = ''
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
        for n in req.headers:
            if 'X-Auth-User' == n:
                self.userName = req.headers[n]
            if 'X-Auth-Key' == n:
                self.userKey = req.headers[n]
#         aus = Client(auth_url=settings.AUTH_URL,username='admin',password='ADMIN')
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952

        flag = 1
        contianers_in_account = ''
=======
=======
>>>>>>> parent of 32f7b0e... 2013-11-05
<<<<<<< HEAD
=======
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952

        flag = 1
        resheaders = []
        try:
#             def get_auth(url, user, key, tenant_name=None):
            print self.global_conf['AUTH_URL']
            auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
            
            #     file = open('//Users//adrian//Desktop//scloud.sql','rb')
            #     conn.put_object('haha','scloud.sql',file,headers = {})
            resbody=  (Connection(authurl =auth_url, user = self.userName,\
                            key = self.userKey, tenant_name = req.headers['domain']).put_container(req.headers['container']))
            
            
=======
<<<<<<< HEAD
=======
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
            
            #     file = open('//Users//adrian//Desktop//scloud.sql','rb')
            #     conn.put_object('haha','scloud.sql',file,headers = {})
            resbody=  (Connection(authurl =auth_url, user = self.userName,\
                            key = self.userKey, tenant_name = req.headers['domain']).put_container(req.headers['container']))
            
            
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
>>>>>>> parent of 32f7b0e... 2013-11-05
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
#             return [str(contianers_in_account),]
        else:
            start_response("200 OK", [])
#             return ["you are not authenticated"]
        
        return self.content
        
        
    def DELETE(self, environ,start_response):
        req = Request(environ)
        res = Response()

        self.userName = 'x'
        self.userKey = 'x'
        self.token = ''
        self.content = ''
        for n in req.headers:
            if 'X-Auth-User' == n:
                self.userName = req.headers[n]
            if 'X-Auth-Key' == n:
                self.userKey = req.headers[n]
#         aus = Client(auth_url=settings.AUTH_URL,username='admin',password='ADMIN')

        flag = 1
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
>>>>>>> parent of 32f7b0e... 2013-11-05
        resheaders = []
        try:
#             def get_auth(url, user, key, tenant_name=None):
            print self.global_conf['AUTH_URL']
            auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
            resbody,contianers_in_account=  (Connection(authurl =auth_url, user = self.userName,\
                            key = self.userKey, tenant_name = 'admin').get_account())
            
            
            for value in resbody:
                x = (value,resbody[value])
                resheaders.append(x)
#                 print value
            print resheaders
=======
            body=  (Connection(authurl =auth_url, user = self.userName,\
                            key = self.userKey, tenant_name = req.headers['domain']).delete_object(req.headers['container'], req.headers['object']))
            
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
            body=  (Connection(authurl =auth_url, user = self.userName,\
                            key = self.userKey, tenant_name = req.headers['domain']).delete_object(req.headers['container'], req.headers['object']))
            
>>>>>>> parent of 32f7b0e... 2013-11-05
<<<<<<< HEAD
=======
            body=  (Connection(authurl =auth_url, user = self.userName,\
                            key = self.userKey, tenant_name = req.headers['domain']).delete_object(req.headers['container'], req.headers['object']))
            
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
#             print token
#             self.token = token
#             print self.token, self.userKey, self.userName
        except Exception,e:
            flag = 0
            print e
            pass
        if flag:
            start_response("200 OK", resheaders)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
            return [str(contianers_in_account),]
        else:
            return ["you are not authenticated"]
=======
=======
>>>>>>> parent of 32f7b0e... 2013-11-05
<<<<<<< HEAD
=======
>>>>>>> parent of 32f7b0e... 2013-11-05
=======
>>>>>>> bccf4e24273a9ca8ccf11519c8bebbdafed2f952
#             return [str(contianers_in_account),]
        else:
            start_response("404 FileNotFound", [])
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
        
>>>>>>> parent of 32f7b0e... 2013-11-05
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return AccountController(global_conf)
    
    
    
    