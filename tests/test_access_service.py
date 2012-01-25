import unittest
import main
import sqlite3
from api.access_services import AccessService
from datetime import datetime
engine_config = 'sqlite:///test.db'
db_path = 'test.db'

class TestAccessService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
	cls.access_service_obj  = AccessService(engine_config)

    @classmethod
    def tearDownClass(cls):
        cls.access_service_obj.drop_db()

    def setUp(self):
        main.app.config['TESTING'] = True
	self.app = main.app.test_client()
	_db_cleanup()
	self.conn = sqlite3.connect(db_path)
	self.c = self.conn.cursor()

    def tearDown(self):
        self.c.close()
        del self.c
	self.conn.close()

    def testAddService(self):
	self.access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
	self.c.execute("select * from service where code=0")
	self.assertEquals(self.c.fetchone(),(1, 0, "name", "description", 1, "service type", "group"));
	self.c.execute("select keyword from keywords where service_code=0")
	self.assertEquals(self.c.fetchall(),[("keyword1", ),("keyword2", )])

    def testGetServiceList(self):
        self.access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
        self.assertEquals([{"service_code":"0", "service_name":"name", "description":"description", "metadata":"True", "type":"service type", "keywords":"keyword1,keyword2", "group":"group"}], self.access_service_obj.getServiceList())

    def test_add_service_attribute(self):
        self.access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
        self.access_service_obj.add_service_attribute(True, "code", "datatype", True, "datatype_description", 1, "description", 0)
        self.c.execute("select * from attribute where service_code=0")
        self.assertEquals(self.c.fetchone(),(1, 1, "code", "datatype", 1, "datatype_description", 1, "description", 0));
	
    def test_add_service_value(self):
        self.access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
        self.access_service_obj.add_service_value(0, 1, "name", "code")
        self.c.execute("select key, name from 'values' where service_code=0")
        self.assertEquals(self.c.fetchone(),(1, "name"));

    def test_get_service_definition(self):
        self.access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
        self.access_service_obj.add_service_value(0, 1, "name", "code")
        self.access_service_obj.add_service_attribute(True, "code", "datatype", True, "datatype_description", 1, "description", 0)
        self.assertEquals({"service_code":"0", "attributes":{ "attribute":{ "variable":"True", "code":"code", "datatype":"datatype", "required":"True", "datatype_description":"datatype_description", "order":"1", "description":"description", "values":[{"value": {"key":"1", "name":"name"}}]}}}, self.access_service_obj.getServiceDefinition(0))

    def test_add_requests(self):
        self.access_service_obj.add_service(0, "name", "description", True, "", ["keyword1","keyword2"], "group")
        self.access_service_obj.add_service_value(0, 1, "name", "code")
        date = datetime.utcnow()
        self.access_service_obj.add_service_attribute(True, "code", "datatype", True, "datatype_description", 1, "description", 0)
        self.access_service_obj.add_requests(lat = 0.1, long = 0.1, address_string =  "address_string", address_id  = 1, email = "email", device_id = "device_id", account_id = "account_id", first_name = "first_name", last_name = "last_name", phone = 1234567890, description = "description", media_url = "media_url", service_code = 0, status = "open", status_notes = "status_notes", agency_responsible = "agency_responsible", service_notice = "service_notice", zipcode = 111111, expected_datetime = date, requested_datetime = date, updated_datetime = date)
        self.c.execute("select lat, long, address_string, address_id, email, device_id, account_id, first_name, last_name, phone, description, media_url, service_code, status, status_notes, agency_responsible, service_notice, zipcode, expected_datetime , requested_datetime, updated_datetime from requests where id=1")
        self.assertEquals(self.c.fetchone(), (0.1, 0.1, "address_string", 1, "email", "device_id", "account_id", "first_name", "last_name", 1234567890, "description", "media_url", 0, "open", "status_notes", "agency_responsible", "service_notice", 111111, str(date), str(date), str(date)))

    def test_add_requests_id(self):
        self.access_service_obj.add_service(0, "name", "description", True, "", ["keyword1","keyword2"], "group")
        self.access_service_obj.add_service_value(0, 1, "name", "code")
        date = datetime.utcnow()
        self.access_service_obj.add_service_attribute(True, "code", "datatype", True, "datatype_description", 1, "description", 0)
        self.access_service_obj.add_requests(lat = 0.1, long = 0.1, address_string =  "address_string", address_id  = 1, email = "email", device_id = "device_id", account_id = "account_id", first_name = "first_name", last_name = "last_name", phone = 1234567890, description = "description", media_url = "media_url", service_code = 0, status = "open", status_notes = "status_notes", agency_responsible = "agency_responsible", service_notice = "service_notice", zipcode = 111111, expected_datetime = date, requested_datetime = date, updated_datetime = date)
        self.access_service_obj.add_requests_id(1)
        self.c.execute("select * from requests_id where requests_id=1")
        self.assertEquals(self.c.fetchone(), (1, 1))

    def test_add_requests_token(self):
        self.access_service_obj.add_service(0, "name", "description", True, "", ["keyword1","keyword2"], "group")
        self.access_service_obj.add_service_value(0, 1, "name", "code")
        date = datetime.utcnow()
        self.access_service_obj.add_service_attribute(True, "code", "datatype", True, "datatype_description", 1, "description", 0)
        self.access_service_obj.add_requests(lat = 0.1, long = 0.1, address_string =  "address_string", address_id  = 1, email = "email", device_id = "device_id", account_id = "account_id", first_name = "first_name", last_name = "last_name", phone = 1234567890, description = "description", media_url = "media_url", service_code = 0, status = "open", status_notes = "status_notes", agency_responsible = "agency_responsible", service_notice = "service_notice", zipcode = 111111, expected_datetime = date, requested_datetime = date, updated_datetime = date)
        self.access_service_obj.add_requests_token(1)
        self.c.execute("select * from requests_token where requests_id=1")
        self.assertEquals(self.c.fetchone(), (1, 1))

    def test_add_requests_attribute(self):
        self.access_service_obj.add_service(0, "name", "description", True, "", ["keyword1","keyword2"], "group")
        self.access_service_obj.add_service_value(0, 1, "name", "code")
        date = datetime.utcnow()
        self.access_service_obj.add_service_attribute(True, "code", "datatype", True, "datatype_description", 1, "description", 0)
        self.access_service_obj.add_requests(lat = 0.1, long = 0.1, address_string =  "address_string", address_id  = 1, email = "email", device_id = "device_id", account_id = "account_id", first_name = "first_name", last_name = "last_name", phone = 1234567890, description = "description", media_url = "media_url", service_code = 0, status = "open", status_notes = "status_notes", agency_responsible = "agency_responsible", service_notice = "service_notice", zipcode = 111111, expected_datetime = date, requested_datetime = date, updated_datetime = date)
        self.access_service_obj.add_requests_attribute(1, 1, "1")
        self.c.execute("select * from request_attribute where requests_id=1")
        self.assertEquals(self.c.fetchone(), (1, 1, 1, "1"))

    def test_post_sevice_requests(self):
        self.access_service_obj.add_service(0, "name", "description", False, "", ["keyword1","keyword2"], "group")
        form_data = {'service_code' : 0,'lat' : 0.1,'long' : 0.1,'address_string' : 'address_string','address_id' : 1,'email' : 'email','first_name' : 'first_name','last_name' : 'last_name','phone' : 1234567890,'description' : 'description','device_id' : 'device_id', 'account_id' : 'account_id','description' : 'description','media_url' : 'media_url'}
        response = self.access_service_obj.postServiceRequests(form_data)
        self.assertEquals({'service_notice':'Sample service notice', 'account_id':'account_id'}, response)

    def test_get_service_requests(self):
        self.access_service_obj.add_service(0, "name", "description", False, "", ["keyword1","keyword2"], "group")
        date = datetime.utcnow()
        self.access_service_obj.add_requests(lat = 0.1, long = 0.1, address_string =  "address_string", address_id  = 1, email = "email", device_id = "device_id", account_id = "account_id", first_name = "first_name", last_name = "last_name", phone = 1234567890, description = "description", media_url = "media_url", service_code = 0, status = "open", status_notes = "status_notes", agency_responsible = "agency_responsible", service_notice = "service_notice", zipcode = 111111, expected_datetime = date, requested_datetime = date, updated_datetime = date)
        self.access_service_obj.add_requests_id(1)
        self.assertEquals([{'status' : 'open', 'status_notes' : 'status_notes', 'service_name' : 'name', 'service_code' : '0', 'description' : 'description', 'agency_responsible' : 'agency_responsible', 'service_notice' : 'service_notice', 'requested_datetime' : str(date), 'updated_datetime' : str(date), 'expected_datetime' : str(date), 'address' : 'address_string', 'address_id' : '1',  'zipcode' : '111111', 'lat' : '0.1', 'long' : '0.1', 'media_url' : 'media_url'}], self.access_service_obj.getServiceRequests(None))

    def test_get_service_request(self):
        self.access_service_obj.add_service(0, "name", "description", False, "", ["keyword1","keyword2"], "group")
        date = datetime.utcnow()
        self.access_service_obj.add_requests(lat = 0.1, long = 0.1, address_string =  "address_string", address_id  = 1, email = "email", device_id = "device_id", account_id = "account_id", first_name = "first_name", last_name = "last_name", phone = 1234567890, description = "description", media_url = "media_url", service_code = 0, status = "open", status_notes = "status_notes", agency_responsible = "agency_responsible", service_notice = "service_notice", zipcode = 111111, expected_datetime = date, requested_datetime = date, updated_datetime = date)
        self.access_service_obj.add_requests_id(1)
        self.assertEquals({'status' : 'open', 'status_notes' : 'status_notes', 'service_name' : 'name', 'service_code' : '0', 'description' : 'description', 'agency_responsible' : 'agency_responsible', 'service_notice' : 'service_notice', 'requested_datetime' : str(date), 'updated_datetime' : str(date), 'expected_datetime' : str(date), 'address' : 'address_string', 'address_id' : '1',  'zipcode' : '111111', 'lat' : '0.1', 'long' : '0.1', 'media_url' : 'media_url'}, self.access_service_obj.getServiceRequest(1))


def _db_cleanup():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM keywords")
    c.execute("DELETE FROM service")
    c.execute("DELETE FROM attribute")
    c.execute("DELETE FROM 'values'")
    c.execute("DELETE FROM requests")
    c.execute("DELETE FROM requests_id")
    c.execute("DELETE FROM requests_token")
    c.execute("DELETE FROM request_attribute")
    c.close()
    del c
    conn.commit()
    conn.close()
