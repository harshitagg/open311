from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from settings import DATABASE_URI
from service_schema import *

class AccessService:

	def __init__(self, engine_uri):
		engine = create_engine(engine_uri, echo=True)
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

	def add_service_attribute(self, variable, code, datatype, required, datatype_description, order, description, service_code):
		session = self.Session()
		new_attribute = Attributes(variable, code, datatype, required, datatype_description, order, description, service_code)
		session.add(new_attribute)
		session.commit()

	def add_service_value(self,service_code, key, name):
		session = self.Session()
		new_value = Values(service_code, key, name)
		session.add(new_value)
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

	def getServiceDefinition(self, service_code):
		session = self.Session()
		value_list = []
		for row in session.query(Values.key,Values.name).filter(service_code == Values.service_code):
			value_list.append({'value':{'key':str(row.key), 'name':str(row.name)}})
		for attr in session.query(Attributes.variable, Attributes.code, Attributes.datatype, Attributes.required, Attributes.datatype_description, Attributes.order, Attributes.description).filter(service_code == Attributes.service_code):
			return ({'service_code':str(service_code),'attributes':{'attribute':{'variable':str(attr.variable), 'code':str(attr.code), 'datatype':str(attr.datatype), 'required':str(attr.required), 'datatype_description':str(attr.datatype_description), 'order':str(attr.order), 'description':str(attr.description), 'values':value_list}}})
		return []
