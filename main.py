from flask import Flask, request

from api.discovery import ServiceDiscovery
from api.services import ServiceList, ServiceDefinition, ServiceRequests, ServiceRequest, RequestIdFromToken
from webapp.add_service import show_add_serv_form, show_add_serv_def_form

#configuration
SECRET_KEY = 'development'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/services.<format>")
def service_list(format='xml'):
    service_list = ServiceList(format.lower())
    return response_from(service_list.get(), service_list.content_type())

@app.route("/services/<service_code>.<format>")
def service_definition(service_code, format='xml'):
    service_definition = ServiceDefinition(service_code, format.lower())
    return response_from(service_definition.get(), service_definition.content_type())

@app.route("/discovery.<format>")
def discovery(format='xml'):
    if format.lower() not in ['xml', 'json']:
        return "Un-Supported format"       #FIXME This needs to be implemented as per-spec. I am not sure what the spec is at the moment.
    discovery  = ServiceDiscovery(format.lower())
    return response_from(discovery.get(), discovery.content_type())

@app.route("/requests.<format>", methods = ['POST', 'GET'])
def service_requests(format='xml'):
    service_requests = ServiceRequests(format.lower())
    if request.method=='GET':
        return response_from(service_requests.get(request.args), service_requests.content_type())
    else:
        return response_from(service_requests.post(request.form), service_requests.content_type())

@app.route("/tokens/<token_id>.<format>")
def request_id(token_id , format='xml'):
    request_id = RequestIdFromToken(token_id, format.lower())
    return response_from(request_id.get(), request_id.content_type())

@app.route("/requests/<service_request_id>.<format>")
def service_request(service_request_id, format='xml'):
    service_request = ServiceRequest(service_request_id, format.lower())
    return response_from(service_request.get(), service_request.content_type())

@app.route("/add_service", methods = ['POST', 'GET'])
def show_service_form():
    return show_add_serv_form()

@app.route("/add_service_definition", methods = ['POST', 'GET'])
def show_service_def_form():
    return show_add_serv_def_form()

def response_from(body, content_type):
    response = app.make_response(body)
    response.headers['Content-Type'] = content_type
    return response

if __name__ == "__main__":
    app.run(debug=True)
