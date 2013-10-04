# -*- coding: utf-8 -*-
'''
Created on 2013年9月28日

@author: adrian
'''
import os
import webob
from webob import Request
from webob import Response
from paste.deploy import loadapp
from wsgiref.simple_server import make_server

from api.swift import swiftAPI
#Filter
class AuthFilter():
    def __init__(self,app):
        self.app = app
        pass
    def __call__(self,environ,start_response):
        req = Request(environ)
        res = Response()
        
        self.userName = ''
        self.userKey = ''
        self.token = ''
        
        for n in req.headers:
            if 'X-Auth-User' == n:
                self.userName = str(req.headers[n]).strip()
            if 'X-Auth-Key' == n:
                self.userKey = str(req.headers[n]).strip()
#         aus = Client(auth_url=settings.AUTH_URL,username='admin',password='ADMIN')
        try:
            
            auth_url =  str(self.app.global_conf['AUTH_URL']).strip("'")
            url, self.token =  swiftAPI.Connection(authurl =auth_url, user = self.userName, key = self.userKey, tenant_name = 'admin')\
            .get_auth()         
               
        except Exception,e:
            print e
        
        if self.token:
            req.headers['token'] = self.token
            return self.app(environ,start_response)
        else:
            start_response("403 AccessDenied",[("Content-type", "text/plain"),
                                         ])
            return ''
    @classmethod
    def factory(cls, global_conf, **kwargs):
        print "in LogFilter.factory", global_conf, kwargs
        return AuthFilter