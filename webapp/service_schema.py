from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
#from settings import DATABASE_URI
Base = declarative_base()
class Service(Base):
        __tablename__='service'

        code= Column(Integer, primary_key=True)
        name= Column(String, nullable=False)
        descn= Column(String, nullable=False)
        serv_metadata= Column(Boolean, nullable=False)
        serv_type=Column(String, nullable=False)
        keywords= relationship("Keywords")
        group=Column(String, nullable=False)

        #CheckConstraint('serv_type='realtime'||serv_type='batch'||serv_type='blackbox'',name="type_check")

        def __init__(self, code, name, descn, serv_metadata, serv_type, keywords, group):
                self.code=code
                self.name=name
                self.descn=descn
                self.serv_metadata=serv_metadata
                self.serv_type=serv_type
 #               self.keywords=keywords
                self.group=group
 #       def __repr__(self):
 #               return "Service(%r, %r, %r,%r,%r,%r,%r)" % (self.code,self.name, self.descn, self.metadata,self.serv_type,self.keywords,self.group)

class Keywords(Base):
	__tablename__='keywords'
	id = Column(Integer, primary_key=True, autoincrement=True)
	service_code=Column(Integer, ForeignKey('service.code'))
	keywords=Column(String,nullable=False)

	def __init__(self, code, keywords):
		self.code = code
		self.keywords = keywords
