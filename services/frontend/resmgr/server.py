# -*- coding: utf-8 -*-
'''
Created on 2013年9月22日

@author: adrian
'''

import os
import webob
from webob import Request
from webob import Response

import obj

# from api.keystone.client import Client
# from api.keystone import *

from api.swift.swiftAPI import Connection
from api import settings

    

class ResourceServer():
    def __init__(self, global_conf):
        self.global_conf = global_conf
        self.token = ''
        self.userName = ''
        self.userKey = ''
        self.content = ''
        pass
    
    def __call__(self,environ,start_response):
        
        req = Request(environ)
        
        
        
        
        if req.method == 'GET':
            obje = obj()
            
            obje.GET(environ, start_response)
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
        return ResourceServer(global_conf)
    
    
    
    