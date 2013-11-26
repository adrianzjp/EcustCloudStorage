# -*- coding: utf-8 -*-
'''
Created on 2013年11月26日

@author: adrian
'''

# curl   -i -H "X-Auth-Key: abc"  -H "X-Auth-User: abc"  http://localhost:8080/scloud_domain/lb  -X GET

import httplib, urllib
params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
headers = {"X-Auth-Key": "ADMIN",
           "X-Auth-User": "admin"}
conn = httplib.HTTPConnection("localhost:8080")
conn.request("GET", "/scloud_domain/admin", params, headers)
response = conn.getresponse()

print response
print response.status, response.reason
data = response.read()
print data
conn.close()