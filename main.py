from flask import Flask

from flask.ext import SQLAlchemy
from api.discovery import ServiceDiscovery

app = Flask(__name__)


@app.route("/discovery.<format>")
def discovery(format='xml'):
    if format.lower() not in ['xml', 'json']:
        return "Un-Supported format"       #FIXME This needs to be implemented as per-spec. I am not sure what the spec is at the moment.
    
    return (ServiceDiscovery(format.lower())).get()



if __name__ == "__main__":
    app.run()
