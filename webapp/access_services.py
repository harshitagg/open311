from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DATABASE_URI
from service_schema import *

class access_service:

	def __init__(self):
		engine = create_engine('sqlite:///sample.db', echo=True)
		self.Session = sessionmaker()
		self.Session.configure(bind=engine)

	def add_service(self, code, name, descn, serv_metadata, serv_type, keywords, group):
		new_service = Service(code, name, descn, serv_metadata, serv_type, group)
		session = self.Session()
		session.add(new_user)
		for keyword in keywords:
			new_keyword= Keywords(code, keyword)
			session.add(new_keyword)
		session.commit()

	def getServiceList(self):
		session = self.Session()
		keywords = []
		services = []
		for row in session.query(Service.code, Service.name, Service.descn, Service.serv_metadata, Service.serv_type, Service.group).all():
			for keyword in session.query(Keywords.keywords).filter(Keywords.code==row.code):
				keyword.append(Keywords.keywords)
			services.append(dict(service_code=row.code,service_name=row.name, description=row.descn,metadata=row.serv_metadata,type=row.serv_type,keywords=keywords,group=row.group))
		return services
