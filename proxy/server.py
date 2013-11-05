# -*- coding: utf-8 -*-
'''
Created on 2013年9月11日

@author: adrian
'''
'''
Created on 2011-6-12
@author: Sonic
'''
import os
import webob
from webob import Request
from webob import Response
from paste.deploy import loadapp
from wsgiref.simple_server import make_server


if __name__ == '__main__':
    configfile="config.ini"
    appname="pdl"
    wsgi_app = loadapp("config:%s" % os.path.abspath(configfile), appname)
    server = make_server('localhost',8080,wsgi_app)
    server.serve_forever()
    pass