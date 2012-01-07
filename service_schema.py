# vim: ai ts=4 sts=4 et sw= encoding=utf-8
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
#from settings import DATABASE_URI

Base = declarative_base()

class Service(Base):
        __tablename__='service'

        code = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
        descn = Column(String, nullable=False)
        serv_metadata = Column(Boolean, nullable=False)
        serv_type = Column(String, nullable=False)
        group = Column(String, nullable=False)

        #CheckConstraint('serv_type='realtime'||serv_type='batch'||serv_type='blackbox'',name="type_check")

        def __init__(self, code, name, descn, serv_metadata, serv_type, group):
                self.code=code
                self.name=name
                self.descn=descn
                self.serv_metadata=serv_metadata
                self.serv_type=serv_type
                self.group=group
 #       def __repr__(self):
 #               return "Service(%r, %r, %r,%r,%r,%r,%r)" % (self.code,self.name, self.descn, self.metadata,self.serv_type,self.keywords,self.group)


class Keywords(Base):
	__tablename__='keywords'
	id = Column(Integer, primary_key = True, autoincrement = True)
	service_code = Column(Integer, ForeignKey('service.code'))
	keyword = Column(String,nullable=False)

	def __init__(self, service_code, keyword):
		self.service_code = service_code
		self.keyword = keyword


class Values(Base):
	__tablename__ = 'values'
	key = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	service_code = Column(Integer, ForeignKey('service.code'))

	def __init__(self, service_code, key, name):
		self.service_code = service_code
		self.key = key
		self.name = name

class Attributes(Base):
	__tablename__ = 'attribute'
	variable = Column(Boolean, nullable = False)
	code = Column(String, primary_key = True)
	datatype = Column(String, nullable = False)
	required = Column(Boolean, nullable = False)
	datatype_description = Column(String)
	order = Column(Integer, nullable = False)
	description = Column(String, nullable = False)
	service_code = Column(Integer, ForeignKey('service.code'))

	def __init__(self, variable, code, datatype, required, datatype_description, order, description, service_code):
		self.variable = variable
		self.code = code
		self.datatype = datatype
		self.required = required
		self.datatype_description = datatype_description
		self.order = order
		self.description = description
		self.service_code = service_code
		
class DbBase():
	def __init__(self, engine):
		self.engine = engine

	def create(self):
		Base.metadata.create_all(self.engine)

	def drop(self):
		Base.metadata.drop_all(self.engine)
