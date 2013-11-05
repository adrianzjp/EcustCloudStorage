'''

@author: jipingzh
'''

import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import datetime
#SQLAlchemy
# engine = create_engine('sqlite:///meta.db', echo=True)
engine = create_engine('mysql+mysqldb://root:123@localhost/scloud')
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))

class Data(Base):
    __tablename__ = 'data'

#     path = Column(String, primary_key=True)
#     name = Column(String)
    id = Column(Integer, primary_key=True)
    m_content_type = Column(String, nullable=False)
    m_parent_id = Column(Integer, nullable=False, default=0)
    m_name = Column(String, nullable=False)
    m_storage_name = Column(String, nullable=False)
    m_tenant_name = Column(String, nullable=False)
    m_status = Column(String, nullable=False)
    m_url = Column(String, nullable=False)
    m_hash = Column(String, nullable=False)
    m_size = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    def __init__(self, m_name, m_storage_name, m_domain_name, m_content_type, m_status, m_uri, m_hash, m_size, \
                     m_parent_id, created):
            self.m_name = m_name
            self.m_storage_name = m_storage_name
            self.m_tenant_name = m_domain_name
            self.m_content_type = m_content_type
            self.m_status = m_status
            self.m_url = m_uri
            self.m_hash = m_hash
            self.m_size = m_size
            self.m_parent_id = m_parent_id
            self.created = created

    def __repr__(self):
        return '{"id":"%s", "m_content_type":"%s", "m_parent_id":"%s", "m_name":"%s", "m_storage_name":"%s", "m_content_type":"%s", "m_status":"%s", "m_hash":"%s", "created":"%s", "m_domain_name":"%s","m_url": "%s"}' % (self.id, self.m_content_type, self.m_parent_id, self.m_name, self.m_storage_name, \
                         self.m_content_type, self.m_status, self.m_hash, self.created, self.m_tenant_name, \
                         self.m_url)



def transactional(fn):
    """add transactional semantics to a method."""

    def transact(self, **args):
        session = Session()
        try:
            if fn.__name__ == 'get_by_kwargs':
                return fn(self, session, **args)
            else:
                fn(self, session, **args)
            session.commit()
        except Exception, e:
            print e
            session.rollback()
            raise
    transact.__name__ = fn.__name__
    return transact


class DataLogic(object):
    """Performs Actions based on mask values"""
    
    def __init__(self):
        pass

    @transactional
    def add_data(self, session, **kwargs):
        create_record = Data(**kwargs)
        print session.add(create_record)
        
    @transactional
    def delete_data_by_id(self, session, **kwargs):
        idx = kwargs.get('id','')
        delete_record = session.query(Data).filter_by(id=idx).one()
        session.delete(delete_record)
        
    @transactional
    def update_data_by_id(self, session, **kwargs):
        idx = kwargs.get('id','')
        if idx != '':
            kwargs.pop('id')
            session.query(Data).filter_by(id=idx).update(kwargs)
            
    @transactional
    def get_by_kwargs(self, session, **kwargs):
        return session.query(Data).filter_by(**kwargs).all()
        



        

if __name__ == '__main__':
    
    data_opr = DataLogic()
#     add an data
    i = 0
    while i < 10:
        kwargs = {
                      'm_name' : 'hello',
                      'm_storage_name' : 'haha',
                      'm_domain_name' : 'adrian',
                      'm_content_type' : 'obj',
                      'm_status' : '1',
                      'm_uri' : 'hello.zjp',
                      'm_hash' : 'jfalfdjlas',
                      'm_size' : '2G',
                      'm_parent_id' : 0,
                      'created' : datetime.datetime.now(),}      
           
        data_opr.add_data(**kwargs)
        i = i + 1
        
#     delete a data by id
#     kwargs = {'id' : 4}
#     data_opr.delete_data_by_id(**kwargs)
#     
# #     update data by id
#     kwargs = {'id':7, 'm_storage_name':'niuniu', 'm_tenant_name':'hahahaahah'}
#     data_opr.update_data_by_id(**kwargs)
#     
# #     get data by conditions
    kwargs = {'m_name':'haha'}
#     print data_opr.get_by_kwargs(**kwargs)
#     result = str(data_opr.get_by_kwargs(**kwargs)[0])
#     import json
#     print json.loads(result).get('id')
#     print json.loads(result)
    
