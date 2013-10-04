# -*- coding: utf-8 -*-
'''
Created on 2013年9月22日

@author: adrian
'''

from api.swift.swiftAPI import Connection
from api import settings
def test():
#     conn = Connection(authurl = 'http://192.168.1.115:5000/v2.0/',user = 'adrian',key = '111111',tenant_name = 'adrian')
#     
#     print conn.get_auth()
    
#     aus = client.Client(auth_url=AUTH_URL,username='admin',password='ADMIN',tenant_name='admin')
#     print aus.users.findall()
    conn = Connection(authurl =settings.AUTH_URL,user = 'admin',key = 'ADMIN',tenant_name = 'admin')
    conn.put_container('hello', {})
    print conn.head_account()
    
test()