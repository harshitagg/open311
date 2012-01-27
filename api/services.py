# vim: ai ts=4 sts=4 et sw= encoding=utf-8
import json

from open311.utils import content_type_for
from open311.utils import XML
from models import Service

class ServiceList(object):
    def __init__(self, format):
        self.formatter = _xml_formatter_list if format == 'xml' else _json_formatter_list
        self.format = format

    def get(self):
        services = Service.objects
        _services = []
        for service in services:
            _services.append({'service': service.service_list_info()})
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
    access_service_obj = AccessService(engine_config)
    service_definition = access_service_obj.getServiceDefinition(service_code)
    return json.dumps(service_definition)


class ServiceRequests(object):
    def __init__(self, format):
        self.format = format
        self.formatter = _xml_formatter_reqs if format == 'xml' else _json_formatter_reqs

    def get(self, args):
        return self.formatter(args=args, type='get')

    def post(self, form):
        return self.formatter(form=form, type='post')

    def content_type(self):
        return content_type_for(self.format)


def _xml_formatter_reqs(*args, **kwargs):
    root = XML('service_requests')
    access_service_obj = AccessService(engine_config)
    type = kwargs.pop('type')
    subroot = XML('request')

    if(type == 'post'):
        form = kwargs.pop('form')
        post_service_requests = access_service_obj.postServiceRequests(form)
        subroot.append_dict(post_service_requests)
    else:
        args = kwargs.pop('args')
        get_service_requests = access_service_obj.getServiceRequests(args)
        for request in get_service_requests:
            subroot.append_dict(request)

    root.append(subroot)
    return repr(root)


def _json_formatter_reqs(*args, **kwargs):
    content = []
    access_service_obj = AccessService(engine_config)
    type = kwargs.pop('type')

    if(type == 'post'):
        form = kwargs.pop('form')
        post_service_requests = access_service_obj.postServiceRequests(form)
        content.append(post_service_requests)

    else:
        args = kwargs.pop('args')
        get_service_requests = access_service_obj.getServiceRequests(args)
        for request in get_service_requests:
            content.append(request)

    return json.dumps(content)


class ServiceRequest(object):
    def __init__(self, service_request_id, format):
        self.service_request_id = service_request_id
        self.format = format
        self.formatter = _xml_formatter_req if format == 'xml' else _json_formatter_req

    def get(self):
        return self.formatter(self.service_request_id)

    def content_type(self):
        return content_type_for(self.format)

def _xml_formatter_req(service_request_id):
    root = XML('service_requests')
    access_service_obj = AccessService(engine_config)
    subroot = XML('request')
    get_service_request = access_service_obj.getServiceRequest(service_request_id)
    subroot.append_dict(get_service_request)
    root.append(subroot)
    return repr(root)

def _json_formatter_req(service_request_id):
    access_service_obj = AccessService(engine_config)
    get_service_request = access_service_obj.getServiceRequest(service_request_id)
    return json.dumps(get_service_request)


class RequestIdFromToken(object):
    def __init__(self, token_id, format):
        self.token_id = token_id
        self.format = format
        self.formatter = _xml_formatter_token if format == 'xml' else _json_formatter_token

    def get(self):
        return self.formatter(self.token_id)

    def content_type(self):
        return content_type_for(self.format)


def _xml_formatter_token(token_id):
    root = XML('service_requests')
    access_service_obj = AccessService(engine_config)
    subroot = XML('request')
    get_request_id = access_service_obj.getRequestIdFromToken(token_id)
    subroot.append_dict(get_request_id)
    root.append(subroot)
    return repr(root)

def _json_formatter_token(token_id):
    access_service_obj = AccessService(engine_config)
    get_request_id = access_service_obj.getRequestIdFromToken(token_id)
    return json.dumps(get_request_id)
