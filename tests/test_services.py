import unittest

import main

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
