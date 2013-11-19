# -*- coding: utf-8 -*-
'''
Created on 2013年10月10日

@author: adrian
'''


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
class ControllerFilter():
    def __init__(self,app):
        self.app = app
        pass
    def __call__(self,environ,start_response):
        req = Request(environ)
        res = Response()
        
        
        self.userName = ''
        self.userKey = ''
        self.token = ''
        
        url_path = req.path.strip('/').split('/')
        
        if url_path[0]=='scloud_domain':
            req.headers['domain'] = url_path[1]
            
            return self.app(environ,start_response)
        
        elif url_path[0] == 'scloud_container':
            req.headers['domain'] = url_path[1]
            req.headers['container'] = url_path[2:]
            
            return self.app(environ,start_response)
        
        elif url_path[0] == 'scloud_object':
            req.headers['domain'] = url_path[1]
            req.headers['container'] = url_path[2:-1]
            req.headers['object'] = url_path[-1]
            
            return self.app(environ,start_response)
        
        elif url_path[0] == 'scloud_user':
            req.headers['domain'] = url_path[1]
            req.headers['container'] = url_path[2:-1]
            req.headers['object'] = url_path[-1]
            
            return self.app(environ,start_response)
            
        else:
            start_response("403 AccessDenied",[("Content-type", "text/plain"),
                                         ])
            return ''
        
#         print url_path
        
        
        
        return self.app(environ,start_response)
    @classmethod
    def factory(cls, global_conf, **kwargs):
        print "in LogFilter.factory", global_conf, kwargs
        return ControllerFilter