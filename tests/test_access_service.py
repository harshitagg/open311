import unittest
import main
import sqlite3
from api.access_services import AccessService

engine_config = 'sqlite:///test.db'
db_path = 'test.db'

class TestAccessService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
	main.app.config['TESTING'] = True
	self.app = main.app.test_client()
	_db_cleanup()
	self.access_service_obj  = AccessService(engine_config)
	self.conn = sqlite3.connect(db_path)
	self.c = self.conn.cursor()

    def tearDown(self):
        self.c.close()
        del self.c
	self.conn.close()

    def testAddService(self):
	self.access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
	self.c.execute("select * from service where code=0")
	self.assertEquals(self.c.fetchone(),(0,"name", "description", 1, "service type", "group"));
	self.c.execute("select keyword from keywords where service_code=0")
	self.assertEquals(self.c.fetchall(),[("keyword1", ),("keyword2", )])

    def testGetServiceList(self):
        self.access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
        self.assertEquals([{"service_code":"0", "service_name":"name", "description":"description", "metadata":"True", "type":"service type", "keywords":"keyword1,keyword2", "group":"group"}], self.access_service_obj.getServiceList())

    def test_add_service_attribute(self):
        self.access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
        self.access_service_obj.add_service_attribute(True, "code", "datatype", True, "datatype_description", 1, "description", 0)
        self.c.execute("select * from attribute where service_code=0")
        self.assertEquals(self.c.fetchone(),(1,"code", "datatype", 1, "datatype_description", 1, "description", 0));
	
    def test_add_service_value(self):
        self.access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
        self.access_service_obj.add_service_value(0, 1, "name")
        self.c.execute("select key, name from 'values' where service_code=0")
        self.assertEquals(self.c.fetchone(),(1, "name"));

    def test_get_service_definition(self):
        self.access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
        self.access_service_obj.add_service_value(0, 1, "name")
        self.access_service_obj.add_service_attribute(True, "code", "datatype", True, "datatype_description", 1, "description", 0)
        self.assertEquals({"service_code":"0", "attributes":{ "attribute":{ "variable":"True", "code":"code", "datatype":"datatype", "required":"True", "datatype_description":"datatype_description", "order":"1", "description":"description", "values":[{"value": {"key":"1", "name":"name"}}]}}}, self.access_service_obj.getServiceDefinition(0))

	
def _db_cleanup():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM keywords") 
    c.execute("DELETE FROM service")
    c.execute("DELETE FROM attribute")
    c.execute("DELETE FROM 'values'")
    c.close()
    del c
    conn.commit()
    conn.close()
