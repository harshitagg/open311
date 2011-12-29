from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from settings import DATABASE_URI
from service_schema import *

class AccessService:

	def __init__(self):
		engine = create_engine('sqlite:///sample.db', echo=True)
		self.Session = sessionmaker()
		self.Session.configure(bind=engine)

	def add_service(self, code, name, descn, serv_metadata, serv_type, keywords, group):
		session = self.Session()
		new_service = Service(code, name, descn, serv_metadata, serv_type, group)
		session.add(new_service)
		for keyword in keywords:
			new_keyword= Keywords(code, keyword)
			session.add(new_keyword)
		session.commit()

	def getServiceList(self):
		session = self.Session()
		keyword_list = []
		service_list = []
		for row in session.query(Service.code, Service.name, Service.descn, Service.serv_metadata, Service.serv_type, Service.group).all():
			for row_ in session.query(Keywords.keyword).filter(Keywords.service_code==row.code):
				keyword_list.append(row_.keyword)
			keyword_string = ','.join(keyword_list) 
			service_list.append({'service_code':str(row.code), 'service_name':str(row.name), 'description':str(row.descn), 'metadata':str(row.serv_metadata), 'type':str(row.serv_type), 'keywords':str(keyword_string), 'group':str(row.group)})
		return service_list
