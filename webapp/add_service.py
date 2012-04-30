from flask import  render_template, request, flash, redirect
from api.access_services import AccessService

#app = Flask(__name__)
#engine_config = 'sqlite:///sample.db'
#engine_config = 'mysql://root@localhost/open311'
engine_config = 'mysql://root:password@localhost/open311'

def show_add_serv_form():
    if request.method == 'POST':
        keywords = []
        access_service_obj = AccessService(engine_config)
        keywords = request.form['keywords'].split(",")
        metadata = str(request.form['metadata'])
        access_service_obj.add_service(request.form['code'], request.form['name'], request.form['description'],
            _str2bool(metadata), request.form['type'], keywords, request.form['group'])
        flash('Submission Successful')
        return redirect('http://localhost:3031/add_service') #should be replaced with url_for
    else:
        return render_template('add_service.html')


def show_add_serv_def_form():
    if request.method == 'POST':
        data = request.form['data']
        return render_template('add_service_definition.html')
    else:
        return render_template('add_service_definition.html')


def _str2bool(value):
    return value.lower() in ("true")
