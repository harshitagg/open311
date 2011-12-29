import json

import yaml
from lxml import etree

from utils import XML
from settings import SERVICE_DISCOVERY_FILE
from utils import content_type_for

class ServiceDiscovery(object):
    
    def __init__(self, format='xml'):
        self.formatter = _xml_formatter if format == 'xml' else _json_formatter
        self.format = format

    def get(self):
        return self.formatter()

    def content_type(self):
        return content_type_for(self.format)

def _xml_formatter():
    contents = _contents_from_yaml()
    element = XML('discovery')
    return repr(element.append_dict(contents))

def _json_formatter():
    return json.dumps(_contents_from_yaml())

def _contents_from_yaml():
    api_endpoint_file = open(SERVICE_DISCOVERY_FILE)
    contents = yaml.load(api_endpoint_file.read())
    api_endpoint_file.close()
    return contents
