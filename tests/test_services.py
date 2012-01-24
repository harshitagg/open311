import unittest
import sqlite3
from api.access_services import AccessService
import main

engine_config = 'sqlite:///sample.db'
db_path = 'sample.db'

class TestServiceList(unittest.TestCase):
    def setUp(self):
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        pass

    def test_services_xml(self):
        response = self.app.get("/services.xml")
        self.assertEquals(200, response.status_code)

    def test_services_xml_content_type(self):
        response = self.app.get("/services.xml")
        self.assertEquals("text/xml; charset=utf-8", response.headers["Content-Type"])

    def test_services_json(self):
        response = self.app.get("/services.json")
        self.assertEquals(200, response.status_code)

    def test_services_json_content_type(self):
        response = self.app.get("/services.json")
        self.assertEquals("application/json; charset=utf-8", response.headers["Content-Type"])


class TestServiceDefinition(unittest.TestCase):
    def setUp(self):
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        pass

    def test_services_def_xml(self):
        response = self.app.get("/services/001.xml")
        self.assertEquals(200, response.status_code)

    def test_service_def_xml_content_type(self):
        response = self.app.get("/services/001.xml")
        self.assertEquals('text/xml; charset=utf-8', response.headers["Content-Type"])

    def test_service_def_json(self):
        response = self.app.get("/services/001.json")
        self.assertEquals(200, response.status_code)

    def test_service_def_json_content_type(self):
        response = self.app.get("/services/001.json")
        self.assertEquals("application/json; charset=utf-8", response.headers["Content-Type"])


class TestServiceRequests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.access_service_obj = AccessService(engine_config)

    @classmethod
    def tearDownClass(cls):
        cls.access_service_obj.drop_db()

    def setUp(self):
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()
        self.form_data = {
            'service_code': 0,
            'lat': 0.1,
            'long': 0.1,
            'address_string': 'address_string',
            'address_id': 1,
            'email': 'email',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': 1234567890,
            'description': 'description',
            'device_id': 'device_id',
            'account_id': 'account_id',
            'description': 'description',
            'media_url': 'media_url'
        }
        self.access_service_obj.add_service(0, "name", "description", False, "realtime", ["keyword1", "keyword2"],
                                            "group")

    def tearDown(self):
        _db_cleanup()

    def test_service_requests_post_xml(self):
        response = self.app.post("/requests.xml", data=self.form_data)
        self.assertEquals(200, response.status_code)

    def test_service_requests_post_json(self):
        response = self.app.post("/requests.json", data=self.form_data)
        self.assertEquals(200, response.status_code)

    def test_service_requests_get_xml(self):
        response = self.app.get("/requests.xml")
        self.assertEquals(200, response.status_code)

    def test_service_requests_get_json(self):
        response = self.app.get("/requests.json")
        self.assertEquals(200, response.status_code)

    def test_service_requests_post_xml_content_type(self):
        response = self.app.post("/requests.xml", data=self.form_data)
        self.assertEquals("text/xml; charset=utf-8", response.headers["Content-Type"])

    def test_service_requests_post_json_content_type(self):
        response = self.app.post("/requests.json", data=self.form_data)
        self.assertEquals("application/json; charset=utf-8", response.headers["Content-Type"])

    def test_service_requests_get_xml_content_type(self):
        response = self.app.get("/requests.xml")
        self.assertEquals("text/xml; charset=utf-8", response.headers["Content-Type"])

    def test_service_requests_get_json_content_type(self):
        response = self.app.get("/requests.json")
        self.assertEquals("application/json; charset=utf-8", response.headers["Content-Type"])


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
