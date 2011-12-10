from flask import Flask

from api.discovery import ServiceDiscovery
from api.services import ServiceList, ServiceDefinition

app = Flask(__name__)

@app.route("/services.<format>")
def service_list(format='xml'):
    return ServiceList(format).get()

@app.route("/services/<service_code>.<format>")
def service_definition(service_code, format='xml'):
    return ServiceDefinition(service_code, format).get()


@app.route("/discovery.<format>")
def discovery(format='xml'):
    if format.lower() not in ['xml', 'json']:
        return "Un-Supported format"       #FIXME This needs to be implemented as per-spec. I am not sure what the spec is at the moment.
    
    return (ServiceDiscovery(format.lower())).get()



if __name__ == "__main__":
    app.run()
