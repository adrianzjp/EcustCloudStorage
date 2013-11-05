# -*- coding: utf-8 -*-
'''
Created on 2013年10月22日

@author: adrian
'''

from  eventlet.greenpool import GreenPool

# def worker(line):
#     return line
# pool = GreenPool()
# for result in pool.imap(worker, open("scloud_auth.sql", 'r')):
#     print result


for n in open("scloud_auth.sql", 'r'):
    print n
