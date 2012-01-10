# vim: ai ts=4 sts=4 et sw= encoding=utf-8
import json
from utils import content_type_for
from api.access_services import AccessService
from utils import XML
from lxml import etree

engine_config = 'sqlite:///sample.db'

class ServiceList(object):

    def __init__(self, format):
        self.formatter = _xml_formatter_list if format == 'xml' else _json_formatter_list
        self.format = format

    def get(self):
        return self.formatter()

    def content_type(self):
        return content_type_for(self.format)

def _xml_formatter_list():
    root = XML('services')
    access_service_obj = AccessService(engine_config)
    service_list = access_service_obj.getServiceList()
    for service in service_list:
        root.append(XML('service').append_dict(service))
    return repr(root)

def _json_formatter_list():
    content = []
    access_service_obj = AccessService(engine_config)
    service_list = access_service_obj.getServiceList()
    for service in service_list:
        content.append(service)
    return json.dumps(content)

class ServiceDefinition(object):

    def __init__(self, service_code, format):
        self.service_code = service_code
        self.format = format
        self.formatter = _xml_formatter_def if format == 'xml' else _json_formatter_def
       
    def get(self):
        return self.formatter(self.service_code)

    def content_type(self):
        return content_type_for(self.format)

def _xml_formatter_def(service_code):
    root = XML('service_definition')
    access_service_obj = AccessService(engine_config)
    service_definition = access_service_obj.getServiceDefinition(service_code)
    root.append_dict(service_definition)
    return repr(root)

def _json_formatter_def(service_code):
    content = []
    access_service_obj = AccessService(engine_config)
    service_definition = access_service_obj.getServiceDefinition(service_code)
    return json.dumps(service_definition)

class ServiceRequest(object):

    def get(self):
        pass

    def post(self):
        pass

class MultipleServiceRequest(object):

    def get(self):
        pass
