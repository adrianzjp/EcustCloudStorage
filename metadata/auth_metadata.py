# -*- coding: utf-8 -*-
'''
Created on 2013年9月27日

@author: adrian
'''
import MySQLdb
from api import settings
import hashlib 


def getConn(database):
    conn = MySQLdb.connect(host=settings.HOST_IP, \
                           user="root", \
                           passwd="123", \
                           db=database)
    return conn




def auth(name, pw):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select id,name,email from user where name='"+str(name)+"' and pass='"+str(pw)+"' and is_active=1")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res
    
# users opr

def get_users():
        
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select id, name, is_active from user")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res

def delete_user_by_id(id):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("delete from user where id="+str(id))
    cursor.close()
    conn.close()


def get_user_by_id(id):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select user.id, user.name, user.email, user.created, role.role_name, domain.name, domain_type.type, role.is_active from user left join "+ 
    "user_domain_roles on user.id = user_domain_roles.user_id left join role on role.id = user_domain_roles.role_id left join domain on user_domain_roles.domain_id=domain.id left join domain_type on domain_type.id = domain.domain_type_id where user.id="+str(id))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res

def put_user(**kws):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("insert into user(name,pass,email,is_active,created,modified)"+
                   " values('"+kws['name']+"','"+kws['pw']+"','"+kws['email']+"',1,NOW(),NOW());")
    cursor.close()
    conn.close()
    
def check_user(name):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select * from user where name='"+str(name)+"'")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res
    
#------------------------for role oprs


def get_roles():

    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select id, role_name,is_active, role_type, role_expires, metadata from role")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res

def get_roles_by_domain_type(id):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select role.id, role_name, role_type, role_expires, metadata from role left join roles_in_domain on role.id=roles_in_domain.role_id where roles_in_domain.domain_type_id="+str(id))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res
 


def put_role(**kws):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("insert into role(role_name, role_type, role_expires, is_active)"+
                   " values('"+kws['rname']+"','"+kws['rtype']+"',NOW(),0);")
    cursor.close()
    conn.close()

def delete_role_by_id(id):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("delete from role where id="+str(id))
    cursor.close()
    conn.close()


def get_role_by_id(id):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select id, role_name, role_type, role_expires, is_active, metadata from role where role.id="+str(id))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res

def get_role_by_name(name):    
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select role.role_name from role left join user_domain_roles on role.id = user_domain_roles.role_id left join user on user.id = user_domain_roles.user_id where user.name='"+str(name)+"'")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res
    
def update_role_permissions(role_id,ids):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("UPDATE role SET  is_active=1, metadata ='"+str(ids)+"' where id = "+str(role_id))
    cursor.close()
    conn.close()


def check_role(name):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select * from role where role_name='"+str(name)+"'")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def put_user_domain_roles(user_id, role_id, domain_id):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("insert into user_domain_roles(user_id, domain_id, role_id, created, modified) values("+user_id+", "+domain_id+","+
                   role_id+", NOW(), NOW());")
    cursor.close()
    conn.close()

def check_user_domain_roles(user_id, role_id, domain_id):    
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select * from user_domain_roles where user_id = "+str(user_id)+" and domain_id="+str(domain_id)+" and role_id="+
                   str(role_id))
    res = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return len(res)

#----------for permission

def get_permissions():
    
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select id, name from permission")
    res = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return res


def get_permission_by_ids(ids):
    conn = getConn("scloud")
    cursor = conn.cursor()
    if ids=='all':
        cursor.execute("select name from permission")
    elif ids == '':
        cursor.execute("select name from permission where id = 0")
    else:
        cursor.execute("select name from permission where id in ("+str(ids)+")")
    res = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return res




#--------------------------

#for domain oprs

def get_domain_user_role_by_domain_id(domain_id):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select domain.name, domain_type.type, user_space.name, domain.size, domain.created, "+
                   "user.name, role.role_name, user_domain_roles.is_active, domain_type.id"+
                   " from domain left join user_domain_roles on domain.id = user_domain_roles.domain_id left join role on user_domain_roles.role_id = role.id left join user on user_domain_roles.user_id = user.id left join domain_type on domain_type.id = domain.domain_type_id left join user_space on domain.space_id = user_space.id where domain.id="+str(domain_id))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res



def get_domains():
    
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select id,domain_type_id, name from domain")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res

   
def get_domains_by_domain_type(domain_type_id):
    
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select domain.id,domain.name, user.name, domain.size, domain.is_active from domain left join user_space on domain.space_id = user_space.id left join user on user_space.owner_id = user.id where domain.domain_type_id = "+str(domain_type_id))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res

def get_domains_by_space_id_and_domain_type_id(space_id, domain_type_id):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select domain.id,domain.name, 'x', domain.size, domain.is_active from domain where space_id = "+str(space_id)+" and domain_type_id = "+str(domain_type_id))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res

def put_domain(name, domain_type_id, space_id, size):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("insert into domain(name, domain_type_id, space_id, size, created, modified) values('"+str(name)+"', "+str(domain_type_id)+","+
                   str(space_id)+","+str(size)+", NOW(), NOW());")
    cursor.close()
    conn.close()

    
def delete_domain_by_id(id):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("delete from domain where id="+str(id))
    cursor.close()
    conn.close()

def update_domain_is_active(did, active_code):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("UPDATE domain SET is_active ="+str(active_code)+" where id = "+str(did))
    cursor.close()
    conn.close()
    
#---------------space table

def get_spaces():
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select id,name, owner_id, size,is_active, created, expires, modified from user_space")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res


def get_space_by_user_name(uname):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select user_space.id,user_space.name,user_space.size, user_space.created, user_space.expires from user_space left join user on user_space.owner_id = user.id where user.name = '"+str(uname)+"'")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res
    
def put_space(user_name, size=2):    
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select id from user where name = '"+str(user_name)+"'")
    res = cursor.fetchall()
    user_id = res[0][0]
    
    cursor.execute("insert into user_space(name, owner_id, size, created, expires, modified) values('"+str(user_name)+'_space'+"', "+str(user_id)+","+str(size)+",NOW(), NOW(), NOW());")
    
    cursor.close()
    conn.close()
    
def update_space_by_id(is_active='', size='',sid=0):
    conn = getConn("scloud")
    cursor = conn.cursor()
    if is_active!='' and size!='':
        cursor.execute("UPDATE user_space SET size = "+str(size)+", is_active ="+str(is_active)+" where id = "+str(sid))
    elif is_active!='':
        cursor.execute("UPDATE user_space SET is_active ="+str(is_active)+" where id = "+str(sid))
    elif size!='':
        cursor.execute("UPDATE user_space SET size = "+str(size)+" where id = "+str(sid))
    else:
        raise
    cursor.close()
    conn.close()
    
def check_space(name):
    conn = getConn("scloud")
    cursor = conn.cursor()
    cursor.execute("select * from user_space where name='"+str(name)+"_space'")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(res)


