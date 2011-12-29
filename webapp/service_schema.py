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
	id = Column(Integer, primary_key=True, autoincrement=True)
	service_code = Column(Integer, ForeignKey('service.code'))
	keyword = Column(String,nullable=False)

	def __init__(self, service_code, keyword):
		self.service_code = service_code
		self.keyword = keyword

engine = create_engine('sqlite:///sample.db', echo=True)
Base.metadata.create_all(engine)
