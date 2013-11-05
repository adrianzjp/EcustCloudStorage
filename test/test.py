# -*- coding: utf-8 -*-
'''
Created on 2013年10月29日

@author: adrian
'''
import json


teststr = "{'hello': 2, 'haha': 'haha'}"
print json.loads(teststr).get('hello')