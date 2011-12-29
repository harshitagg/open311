from lxml import etree
import unittest
import utils

class UtilTests(unittest.TestCase):
    
    def test_xml_append_dict(self):
        dictionary = {'foo':'bar', 'changeset':'2011-12-12','endpoints': {
            'specification':'wewew', 'type':'production'
        }, 'formats':[{'handle': 'pipe'}, {'handle': 'pipe1'}]}
        root = utils.XML('discovery')
        self.assertEquals("""<?xml version='1.0' encoding='utf-8'?>\n<discovery><changeset>2011-12-12</changeset><foo>bar</foo><endpoints><specification>wewew</specification><type>production</type></endpoints><formats><handle>pipe</handle><handle>pipe1</handle></formats></discovery>""", repr(root.append_dict(dictionary)))

    def test_content_type_for_xml(self):
        self.assertEquals('text/xml; charset=utf-8', utils.content_type_for("xml"))

    def test_content_type_for_json(self):
        self.assertEquals('application/json; charset=utf-8', utils.content_type_for("json"))

