# vim: ai ts=4 sts=4 et sw= encoding=utf-8

from sqlalchemy import create_engine, between
from sqlalchemy.orm import sessionmaker
from service_schema import Service, Keywords, Values, Attributes, DbBase, Requests, RequestsId, RequestsToken, RequestAttribue
from flask import abort
from datetime import datetime, timedelta

class AccessService(object):
    def __init__(self, engine_uri):
        engine = create_engine(engine_uri, echo=True)
        self.db_base = DbBase(engine)
        self.db_base.create()
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)

    def drop_db(self):
        self.db_base.drop()

    def add_service(self, code, name, descn, serv_metadata, serv_type, keywords, group):
        session = self.Session()
        new_service = Service(code=code, name=name, descn=descn, serv_metadata=serv_metadata, serv_type=serv_type,
                              group=group)
        session.add(new_service)
        for keyword in keywords:
            new_keyword = Keywords(service_code=code, keyword=keyword)
            session.add(new_keyword)
        session.commit()

    def add_service_attribute(self, variable, code, datatype, required, datatype_description, order, description,
                              service_code):
        session = self.Session()
        new_attribute = Attributes(variable=variable, code=code, datatype=datatype, required=required,
                                   datatype_description=datatype_description, order=order, description=description,
                                   service_code=service_code)
        session.add(new_attribute)
        session.commit()

    def add_service_value(self, service_code, key, name, attribute_code):
        session = self.Session()
        new_value = Values(service_code=service_code, key=key, name=name, attribute_code=attribute_code)
        session.add(new_value)
        session.commit()

    def add_requests(self, *args, **kwargs):
        session = self.Session()
        new_request = Requests(lat=kwargs.pop('lat', None), long=kwargs.pop('long', None),
                               address_string=kwargs.pop('address_string', None),
                               address_id=kwargs.pop('address_id', None), email=kwargs.pop('email', None),
                               device_id=kwargs.pop('device_id', None), account_id=kwargs.pop('account_id', None),
                               first_name=kwargs.pop('first_name', None), last_name=kwargs.pop('last_name', None),
                               phone=kwargs.pop('phone', None), media_url=kwargs.pop('media_url', None),
                               status=kwargs.pop('status', None), status_notes=kwargs.pop('status_notes', None),
                               service_code=kwargs.pop('service_code', None),
                               description=kwargs.pop('description', None),
                               agency_responsible=kwargs.pop('agency_responsible', None),
                               service_notice=kwargs.pop('service_notice', None),
                               requested_datetime=kwargs.pop('requested_datetime', None),
                               updated_datetime=kwargs.pop('updated_datetime', None),
                               expected_datetime=kwargs.pop('expected_datetime', None),
                               zipcode=kwargs.pop('zipcode', None))
        session.add(new_request)
        session.commit()

    def add_requests_id(self, requests_id):
        session = self.Session()
        new_request_id = RequestsId(requests_id=requests_id)
        session.add(new_request_id)
        session.commit()

    def add_requests_token(self, requests_id):
        session = self.Session()
        new_request_token = RequestsToken(requests_id=requests_id)
        session.add(new_request_token)
        session.commit()

    def add_requests_attribute(self, requests_id, attribute_code, value):
        session = self.Session()
        new_request_attribute = RequestAttribue(requests_id=requests_id, attribute_code=attribute_code, value=value)
        session.add(new_request_attribute)
        session.commit()

    def getServiceList(self):
        session = self.Session()
        service_list = []
        for row in session.query(Service.code, Service.name, Service.descn, Service.serv_metadata, Service.serv_type,
                                 Service.group).all():
            keyword_list = []
            for row_ in session.query(Keywords.keyword).filter(Keywords.service_code == row.code):
                keyword_list.append(row_.keyword)
            keyword_string = ','.join(keyword_list)
            service_list.append(
                    {'service_code': str(row.code), 'service_name': str(row.name), 'description': str(row.descn),
                     'metadata': str(row.serv_metadata), 'type': str(row.serv_type), 'keywords': str(keyword_string),
                     'group': str(row.group)})
        return service_list

    def getServiceDefinition(self, service_code):
        if service_code is None:
            abort(400)

        session = self.Session()
        value_list = []
        for row in session.query(Values.key, Values.name).filter(service_code == Values.service_code):
            value_list.append({'value': {'key': str(row.key), 'name': str(row.name)}})
        for attr in session.query(Attributes.variable, Attributes.code, Attributes.datatype, Attributes.required,
                                  Attributes.datatype_description, Attributes.order, Attributes.description).filter(
            service_code == Attributes.service_code):
            return ({'service_code': str(service_code), 'attributes': {
                'attribute': {'variable': str(attr.variable), 'code': str(attr.code), 'datatype': str(attr.datatype),
                              'required': str(attr.required), 'datatype_description': str(attr.datatype_description),
                              'order': str(attr.order), 'description': str(attr.description), 'values': value_list}}})
        abort(404)

    def postServiceRequests(self, request_form):
        print request_form
        service_code = request_form['service_code']
        print service_code
        if(service_code is None):
            abort(400)

        session = self.Session()
        serv_metadata = False
        service_found = False
        for row in session.query(Service.serv_type, Service.serv_metadata).filter(service_code == Service.code):
            serv_type = row.serv_type
            serv_metadata = row.serv_metadata
            service_found = True

        if(not service_found):
            abort(404)

        if(serv_metadata):
            attributes = request_form.getlist('attribute')
            if(attributes is None):
                abort(400)

        self.add_requests(lat=request_form['lat'], long=request_form['long'],
                          address_string=request_form['address_string'], address_id=request_form['address_id'],
                          email=request_form['email'], device_id=request_form['device_id'],
                          account_id=request_form['account_id'], first_name=request_form['first_name'],
                          last_name=request_form['last_name'], phone=request_form['phone'],
                          description=request_form['description'], media_url=request_form['media_url'],
                          service_code=service_code, status='open')

        for row in session.query(Requests.id).filter(service_code == Requests.service_code):
            id = row.id

        if(serv_metadata):
            for code, values in attributes:
                for value in values:
                    self.add_requests_attribute(requests_id=id, attribute_code=code, value=value)

        if(serv_type.lower() == "realtime"):
            self.add_requests_id(requests_id=id)
            for row in session.query(RequestsId.service_request_id).filter(id == RequestsId.requests_id):
                service_request_id = row.service_request_id
            return ({'service_request_id': str(service_request_id), 'service_notice': 'Sample service notice',
                     'account_id': str(request_form['account_id'])})

        elif (serv_type.lower() == "batch"):
            self.add_requests_token(requests_id=id)
            for row in session.query(RequestsToken.token).filter(id == RequestsToken.requests_id):
                token = row.token
            return ({'token': str(token), 'service_notice': 'Sample service notice',
                     'account_id': str(request_form['account_id'])})

        else:
            return ({'service_notice': 'Sample service notice', 'account_id': request_form['account_id']})

    def getServiceRequests(self, args):
        try:
            service_request_id_list = args.getlist['service_request_id']
        except (TypeError, ValueError, AttributeError):
            service_request_id_list = None

        try:
            service_code_list = args.getlist['service_code']
        except (TypeError, ValueError, AttributeError):
            service_code_list = None

        try:
            end_date = args.get['end_date']
        except (TypeError, ValueError, AttributeError):
            end_date = datetime.utcnow()

        try:
            start_date = args.get['end_date']
        except (TypeError, ValueError, AttributeError):
            start_date = (end_date - timedelta(days=90))

        try:
            status_list = args.getlist['status']
        except (TypeError, ValueError, AttributeError):
            status_list = None

        session = self.Session()
        requests_list = []
        request_id_list = []

        if(service_request_id_list is not None):
            for row in session.query(RequestsId.requests_id).filter(
                RequestsId.service_request_id.in_(service_request_id_list)):
                request_id_list.append(row.requests_id)

        else:
            for row in session.query(RequestsId.requests_id):
                request_id_list.append(row.requests_id)

        if(service_code_list is not None):
            for row in session.query(Requests.id).filter(Requests.id.in_(request_id_list)).filter(
                Requests.service_code.in_(service_code_list)):
                request_id_list.append(row.id)

        for row in session.query(Requests.id).filter(Requests.id.in_(request_id_list)).filter(
            between(Requests.requested_datetime, start_date, end_date)):
            request_id_list.append(row.id)

        if(status_list is not None):
            for row in  session.query(Requests.id).filter(Requests.id.in_(request_id_list)).filter(
                Requests.status.in_(status_list)):
                request_id_list.append(row.id)

        for row in session.query(Requests.status, Requests.status_notes, Service.name, Requests.service_code,
                                 Requests.description, Requests.agency_responsible, Requests.service_notice,
                                 Requests.requested_datetime, Requests.updated_datetime, Requests.expected_datetime,
                                 Requests.address_string, Requests.address_id, Requests.zipcode, Requests.lat,
                                 Requests.long, Requests.media_url).filter(Requests.id.in_(request_id_list)).join(
            Service, Requests.service_code == Service.code).limit(1000):
            requests_list.append(
                    {'status': str(row.status), 'status_notes': str(row.status_notes), 'service_name': str(row.name),
                     'service_code': str(row.service_code), 'description': str(row.description),
                     'agency_responsible': str(row.agency_responsible), 'service_notice': str(row.service_notice),
                     'requested_datetime': str(row.requested_datetime), 'updated_datetime': str(row.updated_datetime),
                     'expected_datetime': str(row.expected_datetime), 'address': str(row.address_string),
                     'address_id': str(row.address_id), 'zipcode': str(row.zipcode), 'lat': str(row.lat),
                     'long': str(row.long), 'media_url': str(row.media_url)})

        return requests_list

    def getServiceRequest(self, service_request_id):
        if service_request_id is None:
            abort(400)

        session = self.Session()
        request_id = None
            
        for row in session.query(RequestsId.requests_id).filter(RequestsId.service_request_id == service_request_id):
            request_id = row.requests_id

        if request_id is None:
            abort(404)

        for row in session.query(Requests.status, Requests.status_notes, Service.name, Requests.service_code,
                                 Requests.description, Requests.agency_responsible, Requests.service_notice,
                                 Requests.requested_datetime, Requests.updated_datetime, Requests.expected_datetime,
                                 Requests.address_string, Requests.address_id, Requests.zipcode, Requests.lat,
                                 Requests.long, Requests.media_url).filter(Requests.id == request_id).join(
            Service, Requests.service_code == Service.code):
            request = {'status': str(row.status), 'status_notes': str(row.status_notes), 'service_name': str(row.name),
                     'service_code': str(row.service_code), 'description': str(row.description),
                     'agency_responsible': str(row.agency_responsible), 'service_notice': str(row.service_notice),
                     'requested_datetime': str(row.requested_datetime), 'updated_datetime': str(row.updated_datetime),
                     'expected_datetime': str(row.expected_datetime), 'address': str(row.address_string),
                     'address_id': str(row.address_id), 'zipcode': str(row.zipcode), 'lat': str(row.lat),
                     'long': str(row.long), 'media_url': str(row.media_url)}

        return request

    def getRequestIdFromToken(self, token_id):
        if token_id is None:
            abort(400)

        session = self.Session()
        requests_id = None
        for row in session.query(RequestsToken.requests_id).filter(RequestsToken.token == token_id):
            requests_id = row.requests_id

        if requests_id is None:
            abort(404)

        session.query(RequestsToken).filter(RequestsToken.token == token_id).delete()
        session.commit()
        self.add_requests_id(requests_id)
        for row in session.query(RequestsId.service_request_id).filter(RequestsId.requests_id == requests_id):
            service_request_id = row.service_request_id

        return {'service_request_id' : str(service_request_id), 'token' : str(token_id)}
