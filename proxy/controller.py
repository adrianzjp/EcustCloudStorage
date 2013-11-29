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
    '''
    
    0.查看 domain[public, protected, private]
    1.创建、查看、罗列、删除 container
    2.修改、获取container的访问权限[public_read, public_read_write, private]
    3.上传、查看、罗列、删除 Object
    4.查看 capability
    
    ----------not finished yet
    5.对于大文件支持分片上传(Multi-Part Upload)
    6.访问时支持If-Modified-Since和If-Match等HTTP参数
    
    例子：
    
    PUT /cdmi_domains/MyDomain/ HTTP/1.1
    Host: cloud.example.com
    Accept: application/cdmi-domain
    Content-Type: application/cdmi-domain
    X-CDMI-Specification-Version: 1.0.2
    {
        "metadata" : {
    } }
    The following shows the response.
    HTTP/1.1 201 Created
    Content-Type: application/cdmi-domain
    X-CDMI-Specification-Version: 1.0.2
    {
        "objectType" : "application/cdmi-domain",
        "objectID" : "00007E7F00104BE66AB53A9572F9F51E",
        "objectName" : "MyDomain/",
        "parentURI" : "/cdmi_domains/",
        "parentID" : "00007E7F0010C058374D08B0AC7B3550",
        "domainURI" : "/cdmi_domains/MyDomain/",
        "capabilitiesURI" : "/cdmi_capabilities/domain/",
        "metadata" : {
        },
        "childrenrange" : "0-1",
        "children" : [
            "cdmi_domain_summary/",
            "cdmi_domain_members/"
        ]
    }
    
    
    PUT /MyContainer/    HTTP/1.1
       Host: cloud.example.com
       Accept: application/cdmi-container
       Content-Type: application/cdmi-container
       X-CDMI-Specification-Version: 1.0.2
       {
           "metadata" : {
    } }
    The following shows the response.
    6.4
    HTTP/1.1 201 Created
    Content-Type: application/cdmi-container
    X-CDMI-Specification-Version: 1.0.2
    {
        "objectType" : "application/cdmi-container",
        "objectID" : "00007E7F00102E230ED82694DAA975D2",
        "objectName" : "MyContainer/",
        "parentURI" : "/",
        "parentID" : "00007E7F0010128E42D87EE34F5A6560",
        "domainURI" : "/cdmi_domains/MyDomain/",
        "capabilitiesURI" : "/cdmi_capabilities/container/",
        "completionStatus" : "Complete",
        "metadata" : {
            "cdmi_size" : "0"
        },
        "childrenrange" : "",
        "children" : [
    ] }    
    
    PUT /MyContainer/MyDataObject.txt HTTP/1.1
    Host: cloud.example.com
    Accept: application/cdmi-object
    Content-Type: application/cdmi-object
    X-CDMI-Specification-Version: 1.0.2
    {
        "mimetype" : "text/plain",
        "metadata" : {
    },
        "value" : "Hello CDMI World!"
    }
    The following shows the response.
    38
    HTTP/1.1 201 Created
    Content-Type: application/cdmi-object
    X-CDMI-Specification-Version: 1.0.2
    {
        "objectType" : "application/cdmi-object",
        "objectID" : "00007E7F0010BD1CB8FF1823CF05BEE4",
        "objectName" : "MyDataObject.txt",
        "parentURI" : "/MyContainer/",
        "parentID" : "00007E7F00102E230ED82694DAA975D2",
        "domainURI" : "/cdmi_domains/MyDomain/",
        "capabilitiesURI" : "/cdmi_capabilities/dataobject/",
        "completionStatus" : "Complete",
        "mimetype" : "text/plain",
        "metadata" : {
            "cdmi_size" : "17"
        }
    }
    
       
    GET /MyContainer/ HTTP/1.1
    Host: cloud.example.com
    Accept: */*
    X-CDMI-Specification-Version: 1.0.2
    The following shows the response.
    HTTP/1.1 200 OK
    Content-Type: application/cdmi-container
       X-CDMI-Specification-Version: 1.0.2
    {
        "objectType" : "application/cdmi-container",
        "objectID" : "00007E7F00102E230ED82694DAA975D2",
        "objectName" : "MyContainer/",
        "parentURI" : "/",
        "parentID" : "00007E7F0010128E42D87EE34F5A6560",
        "domainURI" : "/cdmi_domains/MyDomain/",
        "capabilitiesURI" : "/cdmi_capabilities/container/",
        "completionStatus" : "Complete",
        "metadata" : {
            "cdmi_size" : "83"
        },
        "childrenrange" : "0-0",
        "children" : [
            "MyDataObject.txt"
        ]
    }
    GET /MyContainer/MyDataObject.txt HTTP/1.1
    Host: cloud.example.com
    Accept: application/cdmi-object
    X-CDMI-Specification-Version: 1.0.2
    The following shows the response.
    HTTP/1.1 200 OK
    Content-Type: application/cdmi-object
    X-CDMI-Specification-Version: 1.0.2
    {
    "objectType": "application/cdmi-object",
    "objectID": "00007E7F0010BD1CB8FF1823CF05BEE4",
    "objectName": "MyDataObject.txt",
    "parentURI": "/MyContainer/",
    }
    "parentID" : "00007E7F00102E230ED82694DAA975D2",
    "domainURI": "/cdmi_domains/MyDomain/",
    "capabilitiesURI": "/cdmi_capabilities/dataobject/",
    "completionStatus": "Complete",
    "mimetype": "text/plain",
    "metadata": {
        "cdmi_size": "17"
    },
    "valuetransferencoding": "utf-8",
    "valuerange": "0-16",
    "value": "Hello CDMI World!"
    '''
    
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