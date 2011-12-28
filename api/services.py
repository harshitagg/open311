import json
from utils import content_type_for
from webapp.access_services import access_service
from utils import dict_to_lxml
from lxml import etree

class ServiceList(object):

    def __init__(self, format):
	    self.formatter = _xml_formatter if format == 'xml' else _json_formatter
	    self.format = format

    def get(self):
	return self.formatter()

    def content_type(self):
        return content_type_for(self.format)

def _xml_formatter():
	root = etree.Element('services')
	access_service_obj = access_service()
	service_list = access_service_obj.getServiceList()
	for service in service_list:
		root.append(dict_to_lxml('service',service))
	return etree.tostring(root, encoding='utf-8',xml_declaration=True)

def _json_formatter():
	content=[]
	access_service_obj = access_service()
	service_list = access_service_obj.getServiceList()
	for service in service_list:
		content.append(service)
	return json.dumps(content)

class ServiceDefinition(object):

    def __init__(self, service_code, format):
        self.service_code = service_code
        self.format = format
        
    def get(self):
        pass

class ServiceRequest(object):

    def get(self):
        pass

    def post(self):
        pass

class MultipleServiceRequest(object):

    def get(self):
        pass
