# vim: ai ts=4 sts=4 et sw= encoding=utf-8
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
#from settings import DATABASE_URI

Base = declarative_base()

class Service(Base):
        __tablename__='service'

        id = Column(Integer, primary_key=True)
	code = Column(Integer, nullable=False)
        name = Column(String, nullable=False)
        descn = Column(String, nullable=False)
        serv_metadata = Column(Boolean, nullable=False)
        serv_type = Column(String, nullable=False)
        group = Column(String, nullable=False)


class Keywords(Base):
	__tablename__='keywords'

        id = Column(Integer, primary_key=True)
	service_code = Column(Integer, ForeignKey('service.code'))
	keyword = Column(String,nullable=False)



class Values(Base):
	__tablename__ = 'values'

        id = Column(Integer, primary_key=True)
	key = Column(Integer, nullable=False)
	name = Column(String, nullable = False)
	service_code = Column(Integer, ForeignKey('service.code'))


class Attributes(Base):
	__tablename__ = 'attribute'

        id = Column(Integer, primary_key=True)
	variable = Column(Boolean, nullable = False)
	code = Column(String, nullable=False)
	datatype = Column(String, nullable = False)
	required = Column(Boolean, nullable = False)
	datatype_description = Column(String)
	order = Column(Integer, nullable = False)
	description = Column(String, nullable = False)
	service_code = Column(Integer, ForeignKey('service.code'))

		
class DbBase():
	def __init__(self, engine):
		self.engine = engine

	def create(self):
		Base.metadata.create_all(self.engine)

	def drop(self):
		Base.metadata.drop_all(self.engine)
