'''
Created on 2012-10-27

@author: Adrian
'''
import MySQLdb
from newproject import settings
import hashlib 


def getConn(database):
    conn = MySQLdb.connect(host=settings.HOST_IP, \
                           user="root", \
                           passwd="123456", \
                           db=database)
    return conn


def get_tenants(username):
        
    conn = getConn("keystone")
    cursor = conn.cursor()
    cursor.execute("select tenant.name from tenant left join user_tenant_membership on user_tenant_membership.tenant_id = tenant.id left join user on user.id  = user_tenant_membership.user_id where user.name = '"+username+"'")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res

def put_info(type_name="",tenant_name="",container_name="",file_name="",user_name=""):
    conn = getConn("swiftoprs")
    cursor = conn.cursor()
    cursor.execute("insert into oprs_messages(type,user,tenant,container,file,created) values('"+type_name+"','"+user_name+"','"+tenant_name+"','"+container_name+"','"+file_name+"',NOW())");
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return  res



def put_into_objectdata(m_name="",m_storage_name="",m_tenant_name="",m_content_type="",m_parent_id=0,m_status="",m_url="",m_hash="",m_size=""):
    '''when create a container, we put the container name and some 
    related information into the database to implement the sub folder function
    | Field          | Type             | Null | Key | Default | Extra          |
+----------------+------------------+------+-----+---------+----------------+
| id             | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| m_content_type | varchar(255)     | NO   |     | NULL    |                |
| m_parent_id    | int(10) unsigned | NO   |     | 0       |                |
| m_name         | varchar(255)     | NO   |     |         |                |
| m_storage_name | varchar(255)     | NO   |     |         |                |
| m_tenant_name  | varchar(255)     | NO   |     |         |                |
| m_status       | varchar(255)     | NO   |     |         |                |
| m_url          | varchar(255)     | NO   |     |         |                |
| m_hash         | varchar(255)     | NO   |     |         |                |
| created        | datetime         | NO   |     | NULL    |    
    
    
    '''
    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("insert into dataobject(m_name,m_storage_name,m_tenant_name,m_content_type,m_parent_id,m_status,m_url,m_hash,m_size,created) values('"+m_name+"','"+m_storage_name+"','"+m_tenant_name+"','"+m_content_type+"',"+str(m_parent_id)+",'"+m_status+"','"+m_url+"','"+m_hash+"','"+m_size+"',NOW())");
#    cursor.execute("insert into dataobject(m_name,m_storage_name,m_tenant_name,m_content_type,m_parent_id,m_status,m_url,m_hash,created) values('','','','',0,'','','',NOW())");
    cursor.close()
    conn.close()

def find_container_name(container_staragename):
    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("select m_name from dataobject where m_storage_name = '"+container_staragename+"'");

    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return result[0]


def find_root_id(username):
    
    conn = getConn("openstack")
    cursor = conn.cursor()
    root_container = username+"root"
    root_contaienr_md5 = hashlib.md5(root_container).hexdigest()
    cursor.execute("select id from dataobject where m_storage_name = '"+root_contaienr_md5+"'");

    root_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    
    return root_id


def find_folders_in_rootcontainer(username):
    
    conn = getConn("openstack")
    cursor = conn.cursor()
    root_id = find_root_id(username)
    cursor.execute("select id,m_name,m_storage_name from dataobject where m_parent_id = "+str(root_id)+" and  m_content_type = 'container'");
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return results


def find_objects_in_rootcontainer(username):
    
    conn = getConn("openstack")
    cursor = conn.cursor()
    root_id = find_root_id(username)
    cursor.execute("select id,m_name,m_storage_name,m_size,date_format(created, '%Y/%m/%d %H:%i:%s') from dataobject where m_parent_id = "+str(root_id)+" and  m_content_type = 'object'");
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return results

def findSubContainersById(container_id):
    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("select id,m_name,m_storage_name,m_content_type from dataobject where m_parent_id = "+str(container_id)+" and m_content_type = 'container'");
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return results

def findSubObjectsById(container_id):
    conn = getConn("openstack")
    cursor = conn.cursor()
#    cursor.execute("select id,m_name,m_storage_name,m_content_type from dataobject where m_parent_id = "+str(container_id)+" and m_content_type = 'object'");
    cursor.execute("select id,m_name,m_storage_name,m_size,date_format(created, '%Y/%m/%d %H:%i:%s')  from dataobject where m_parent_id = "+str(container_id)+" and  m_content_type = 'object'");

    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return results
    
    

def get_root_name(username):
    root_container = username+"root"
    root_contaienr_md5 = hashlib.md5(root_container).hexdigest()
    
    return root_contaienr_md5
    

def getNameById(container_id):
    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("select m_storage_name from dataobject where id = "+str(container_id));

    container_sname = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    
    return container_sname    
    

def getIdByName(container_name):
    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("select id from dataobject where m_storage_name = '"+str(container_name)+"'");

    container_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    
    return container_id    
    
def getParentId(container_id):
    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("select m_parent_id from dataobject where id = "+str(container_id));

    container_pid = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    
    return container_pid    


def reName(newname='',id=0):
    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("update dataobject set m_name = '"+newname+"' where id = "+str(id));

    cursor.close()
    conn.close()
    
    
    pass


def deleteContent(content):
    conn = getConn("openstack")
    cursor = conn.cursor()
    content_ids = content.split(',')
    for id in content_ids:
        if id != '':
            cursor.execute("delete from dataobject where id = "+str(id));
        
    cursor.close()
    conn.close()
    

def changeSnameToName(sname,parent_id):

    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("select m_name from dataobject where m_storage_name = '"+sname+"' and m_parent_id="+str(parent_id));

    rname = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    
    return rname    

    
    

#*******************************    
#*******************************    
#*******************************    
#operations on table datashare
#*******************************    
#*******************************    
#*******************************    


def put_into_datashare(m_parent_id=0,m_name="",m_storage_name="",m_tenant_name="",m_content_type="",m_user_from="",m_hash_key="",m_user_to="",m_unique_url="",m_password=""):
    '''when create a container, we put the container name and some 
| Field          | Type             | Null | Key | Default | Extra          |
+----------------+------------------+------+-----+---------+----------------+
| id             | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| m_content_type | varchar(255)     | NO   |     | NULL    |                |
| m_user_from    | varchar(255)     | NO   |     |         |                |
| m_hash_key     | varchar(255)     | NO   |     |         |                |
| m_storage_name | varchar(255)     | NO   |     |         |                |
| m_name         | varchar(255)     | NO   |     |         |                |
| m_tenant_name  | varchar(255)     | NO   |     |         |                |
| m_user_to      | varchar(255)     | NO   |     |         |                |
| m_unique_url   | varchar(255)     | NO   |     |         |                |
| m_password     | varchar(255)     | NO   |     |         |                |
| created        | datetime         | NO   |     | NULL    |   
    
    '''
    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("insert into datashare(m_parent_id,m_name,m_storage_name,m_tenant_name,m_content_type,m_user_from,m_hash_key,m_user_to,m_unique_url,m_password,created) \
    values("+str(m_parent_id)+",'"+m_name+"','"+m_storage_name+"','"+m_tenant_name+"','"+m_content_type+"','"+m_user_from+"','"+m_hash_key+"','"+m_user_to+"','"+m_unique_url+"','"+m_password+"',NOW())");
    cursor.close()
    conn.close()
    
def getShareByUserto(user=''):
    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("select m_unique_url,m_name,m_user_from,date_format(created, '%Y/%m/%d %H:%i:%s') from datashare where m_user_to = '"+user+"' order by id DESC");

    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return results

def getShareMyself(user=''):
    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("select m_unique_url,m_name,m_user_to,date_format(created, '%Y/%m/%d %H:%i:%s') from datashare where m_user_from = '"+user+"' order by id DESC");

    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return results

def getShareByUrl(url=''):
    conn = getConn("openstack")
    cursor = conn.cursor()
    cursor.execute("select m_name,m_parent_id,m_storage_name,m_tenant_name,m_content_type,m_user_from,m_hash_key \
    ,m_password,created from datashare where m_unique_url = '"+url+"' order by id DESC");

    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result

def deleteShare(urls=''):
    conn = getConn("openstack")
    cursor = conn.cursor()
    
    urls = [u for u in urls.split('-') if u!='']
    for url in urls:
        cursor.execute("delete from datashare where m_unique_url = '"+url+"'");

    
    cursor.close()
    conn.close()
    

    
###
if __name__ == '__main__':
    print deleteShare('e_file_20130511154659544000-fasdfaafd-afsdfa-')
