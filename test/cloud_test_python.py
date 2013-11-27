# -*- coding: utf-8 -*-
'''
Created on 2013年11月26日

@author: adrian
'''

# curl   -i -H "X-Auth-Key: abc"  -H "X-Auth-User: abc"  http://localhost:8080/scloud_domain/lb  -X GET

import httplib, urllib
import sys

# params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
params = urllib.urlencode({})

headers = {"X-Auth-Key": "ADMIN",
           "X-Auth-User": "admin"}
conn = httplib.HTTPConnection("localhost:8080")

urls = ["/scloud_object/admin/haha/helloadrianxxx.html","/scloud_container/admin/haha/","/scloud_domain/admin/"]

if sys.argv[1] == 'object':
    test_url = urls[0]
if sys.argv[1] == 'container':
    test_url = urls[1]
if sys.argv[1] == 'domain':
    test_url = urls[2]
    
conn.request("GET", test_url, params, headers)
response = conn.getresponse()

data = response.read()
resheader=response.getheaders()

if test_url.startswith('/scloud_object'):
    savedBinFile = open('/Users/adrian/desktop/test_adrian.html', "wb"); # open a file, if not exist, create it
    savedBinFile.write(data);
    savedBinFile.close();

print '*'*100+""
print 'the headers are'
print '*'*100+"\n"
print resheader
print "\n"
print '*'*100+""
print 'the data is '
print '*'*100+"\n"
print data


conn.close()
