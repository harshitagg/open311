import unittest
import main
import sqlite3
from api.access_services import AccessService

engine_config = 'sqlite:///test.db'
db_path = 'test.db'

class TestAccessService(unittest.TestCase):

    def setup(self):
	main.app.config['TESTING'] = True
	self.app = main.app.test_client()

    def teardown(self):
	pass

    def testAddService(self):
	_db_cleanup()
	access_service_obj  = AccessService(engine_config)
	access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("select * from service where code=0")
	self.assertEquals(c.fetchone(),(0,"name", "description", 1, "service type", "group"));
	c.execute("select keyword from keywords where service_code=0")
	self.assertEquals(c.fetchall(),[("keyword1", ),("keyword2", )])
	c.close()
	del c
	conn.close()

    def testGetServiceList(self):
	_db_cleanup()
	access_service_obj  = AccessService(engine_config)
	access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
	self.assertEquals([{"service_code":"0", "service_name":"name", "description":"description", "metadata":"True", "type":"service type", "keywords":"keyword1,keyword2", "group":"group"}], access_service_obj.getServiceList())

    def test_add_service_attribute(self):
	_db_cleanup()
	access_service_obj  = AccessService(engine_config)
	access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
	access_service_obj.add_service_attribute(True, "code", "datatype", True, "datatype_description", 1, "description", 0)
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("select * from attribute where service_code=0")
	self.assertEquals(c.fetchone(),(1,"code", "datatype", 1, "datatype_description", 1, "description", 0));
	c.close()
	del c
	conn.close()

    def test_add_service_value(self):
	_db_cleanup()
	access_service_obj  = AccessService(engine_config)
	access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
	access_service_obj.add_service_value(0, 1, "name")
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("select key, name from 'values' where service_code=0")
	self.assertEquals(c.fetchone(),(1, "name"));
	c.close()
	del c
	conn.close()

    def test_get_service_definition(self):
	_db_cleanup()
	access_service_obj  = AccessService(engine_config)
	access_service_obj.add_service(0, "name", "description", True, "service type", ["keyword1","keyword2"], "group")
	access_service_obj.add_service_value(0, 1, "name")
	access_service_obj.add_service_attribute(True, "code", "datatype", True, "datatype_description", 1, "description", 0)
	self.assertEquals({"service_code":"0", "attributes":{ "attribute":{ "variable":"True", "code":"code", "datatype":"datatype", "required":"True", "datatype_description":"datatype_description", "order":"1", "description":"description", "values":[{"value": {"key":"1", "name":"name"}}]}}}, access_service_obj.getServiceDefinition(0))

	


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
