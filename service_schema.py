# vim: ai ts=4 sts=4 et sw= encoding=utf-8

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UniqueConstraint, Float, BigInteger, CheckConstraint, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Service(Base):
        __tablename__='service'

        id = Column(Integer, primary_key = True)
	code = Column(Integer, nullable = False, unique = True)
        name = Column(String, nullable = False)
        descn = Column(String, nullable = False)
        serv_metadata = Column(Boolean, nullable = False)
        serv_type = Column(String, nullable = False)
        group = Column(String, nullable = False)


class Keywords(Base):
	__tablename__='keywords'

        id = Column(Integer, primary_key = True)
	service_code = Column(Integer, ForeignKey('service.code'), nullable = False)
	keyword = Column(String,nullable=False)

	UniqueConstraint('service_code', 'keyword', name = 'checkkeywords')


class Values(Base):
	__tablename__ = 'values'

        id = Column(Integer, primary_key = True)
	key = Column(Integer, nullable = False)
	name = Column(String, nullable = False)
	attribute_code = Column(String, ForeignKey('attribute.code'), nullable = False)
	service_code = Column(Integer, ForeignKey('service.code'), nullable = False)
	
	UniqueConstraint('key', 'attribute_code', 'service_code', name = 'checkvalues')


class Attributes(Base):
	__tablename__ = 'attribute'

        id = Column(Integer, primary_key = True)
	variable = Column(Boolean, nullable = False)
	code = Column(String, nullable = False)
	datatype = Column(String, nullable = False)
	required = Column(Boolean, nullable = False)
	datatype_description = Column(String)
	order = Column(Integer, nullable = False)
	description = Column(String, nullable = False)
	service_code = Column(Integer, ForeignKey('service.code'), nullable = False)
	
	UniqueConstraint('code', 'service_code', name = 'checkattributes')


class Requests(Base):
	__tablename__ = 'requests'
	
	id = Column(Integer, primary_key = True)
	lat = Column(Float)
	long = Column(Float)
	address_string = Column(String)
	address_id = Column(Integer)
	email = Column(String)
	device_id = Column(String)
	account_id = Column(String)
	first_name = Column(String)
	last_name = Column(String)
	phone = Column(BigInteger)
	media_url = Column(String)
	status = Column(String,  CheckConstraint("status in('open','close')"), nullable = False)
	status_notes = Column(Text)
	service_code = Column(Integer, ForeignKey('service.code'))
	description = Column(Text)
	agency_responsible = Column(String)
	service_notice = Column(Text)
	requested_datetime = Column(DateTime)
	updated_datetime = Column(DateTime)
	expected_datetime = Column(DateTime)
	zipcode = Column(BigInteger)


class RequestsId(Base):
	__tablename__ = 'requests_id'
	
	service_request_id = Column(Integer, primary_key = True)
	requests_id = Column(Integer, ForeignKey('requests.id'), nullable = False)


class RequestsToken(Base):
	__tablename__ = 'requests_token'

	token = Column(Integer, primary_key = True)
	requests_id = Column(Integer, ForeignKey('requests.id'), nullable = False)


class RequestAttribue(Base):
	__tablename__ = 'request_attribute'

	id = Column(Integer, primary_key = True)
	requests_id = Column(Integer, ForeignKey('requests.id'), nullable = False)
	attribute_code = Column(Integer, ForeignKey('attribute.code'), nullable = False)
	value = Column(String, ForeignKey('values.key'), nullable = False)

	UniqueConstraint('requests_id', 'attribute_code', 'value', name = 'checkrequestattribute')
	

class DbBase():
	def __init__(self, engine):
		self.engine = engine

	def create(self):
		Base.metadata.create_all(self.engine)

	def drop(self):
		Base.metadata.drop_all(self.engine)
