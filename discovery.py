import json

import yaml
from lxml import etree

from utils import dict_to_lxml
from settings import SERVICE_DISCOVERY_FILE

class ServiceDiscovery(object):
    
    def __init__(self, format='xml'):
        self.format = xml_formatter if format == 'xml' else json_formatter

    def get(self):
        return self.format()

def xml_formatter():
    contents = _contents_from_yaml()
    return etree.tostring(dict_to_lxml(etree.Element('discovery'), contents), encoding='utf-8', xml_declaration=True)

def json_formatter():
    return json.dumps(_contents_from_yaml())

def _contents_from_yaml():
    api_endpoint_file = open(SERVICE_DISCOVERY_FILE)
    contents = yaml.load(api_endpoint_file.read())
    api_endpoint_file.close()
    return contents

