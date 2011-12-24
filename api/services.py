from utils import content_type_for

class ServiceList(object):

    def __init__(self, format):
        self.format = format

    def get(self):
        return ""

    def content_type(self):
        return content_type_for(self.format)

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

