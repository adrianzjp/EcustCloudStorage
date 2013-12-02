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

from services.backend.log.log import Log    
import hashlib


from api.swift import swiftAPI
#Filter
class AuthFilter():
    def __init__(self,app):
        self.app = app
        pass
    def __call__(self,environ,start_response):
        req = Request(environ)
        res = Response()
        self.token = ''
        
        #added for production environment
        #the userKey in the header will be encrypted
        #will not cause any security issue
        #--------------
#             self.content_type = req.headers.get('Content-Type', '')
#             #DomainName.scloud.ecust.com
#             self.host = req.headers.get('Host', '')
#             self.cdmi_version = req.headers.get('X-CDMI-Specification-Version', '')
#             self.authorization = req.headers.get('Authorization', '')
#             self.date = req.headers.get('Date', '')
#             self.path = req.path
#             
#             self.key = get the key from the mysql database by the user name
#             
#             key_construct = self.userName+'_'+self.path+'_'+self.date
#             key_md5 = hashlib.md5(key_construct).hexdigest() 
#             
#             if key_md5 == self.userKey:return True
#             
#             return False
        #---------------
        
        
        
        
        # added for test environment
        # the following test mock will be replaced by the above section in production mode
        
        
        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        
#         aus = Client(auth_url=settings.AUTH_URL,username='admin',password='ADMIN')
        try:
            
            auth_url =  str(self.app.global_conf['AUTH_URL']).strip("'")
            url, self.token =  swiftAPI.Connection(authurl =auth_url, user = self.userName, key = self.userKey, tenant_name = req.headers['domain'])\
            .get_auth()         
            Log().info(req.headers.get('X-Auth-User')+' authorized logging in')
               
        except Exception,e:
            print e
            Log().error(req.headers.get('X-Auth-User')+' not authorized to login in, please contact with zhoujip@yeah.net')

            
        
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