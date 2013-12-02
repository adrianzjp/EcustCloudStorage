# -*- coding: utf-8 -*-
'''
Created on 2013年10月10日

@author: adrian
'''

import os
import webob
from webob import Request
from webob import Response
from paste.deploy import loadapp

from proxy.params import *

#Filter
class ControllerFilter():
    
    
    def __init__(self,app):
        self.app = app
        pass
    def __call__(self,environ,start_response):
        '''
        controller here to parse user's http request
        '''
        
        
        #use webob to pack the environment value
        req = Request(environ)
        res = Response()
           
        #here we set a flag value
        #flag == HTTPOk: operation success
        #flag != HTTPOk: operation failed 
        req.headers['http-flag'] = HTTPOk
        #here content type includes scloud-object, scloud-domain, scloud-container, scloud-capability
        #later we may add scloud-queue type
        self.content_type = req.headers.get('Content-Type', '')
        #DomainName.scloud.ecust.com
        self.host = req.headers.get('Host', '')
        self.cdmi_version = req.headers.get('X-CDMI-Specification-Version', '')
        self.authorization = req.headers.get('Authorization', '')
        self.date = req.headers.get('Date', '')
        self.path = req.path
 
        #Make sure req.headers not ""
        if not (self.content_type and self.host and self.cdmi_version and self.date and self.authorization):
            req.headers['http-flag'] = HTTPBadRequest
            return self.app(environ,start_response)
        
        #Set X-Auth-User and X-Auth-Key
        req.headers['X-Auth-User'], req.headers['X-Auth-Key'] = self.authorization.strip().split(':')
        #make sure X-Auth-User and X-Auth-Key not ""
        if not (req.headers['X-Auth-User'] and req.headers['X-Auth-Key']):
            req.headers['http-flag'] = HTTPBadRequest
            return self.app(environ,start_response)
            
        #Make sure content-type is legal
        if self.content_type not in ['scloud-domain', 'scloud-container', 'scloud-object', 'scloud-capability', 'scloud-queue']:
            req.headers['http-flag'] = HTTPBadRequest
            return self.app(environ,start_response)
            
        
        url_path = req.path.strip('/').split('/')
        
        req.headers['url_pattern'] = url_path[0]
        
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
        
        
        
        
    @classmethod
    def factory(cls, global_conf, **kwargs):
        print "in LogFilter.factory", global_conf, kwargs
        return ControllerFilter