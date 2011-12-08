import unittest

import main

class TestServiceEndPoints(unittest.TestCase):

    def setUp(self):
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        pass

    def test_service_discovery_xml(self):
        response = self.app.get('/discovery.xml')
        self.assertEquals(200, response.status_code)

    def test_service_discovery_json(self):
        response = self.app.get('/discovery.json')
        self.assertEquals(200, response.status_code)
