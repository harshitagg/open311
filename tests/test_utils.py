from lxml import etree
import unittest
import utils

class UtilTests(unittest.TestCase):
    
    def test_dict_to_xml(self):
        dictionary = {'foo':'bar', 'changeset':'2011-12-12','endpoints': {
            'specification':'wewew', 'type':'production'
        }, 'formats':[{'handle': 'pipe'}, {'handle': 'pipe1'}]}
        root = etree.Element('discovery')
        self.assertEquals("""<discovery><changeset>2011-12-12</changeset><foo>bar</foo><endpoints><specification>wewew</specification><type>production</type></endpoints><formats><handle>pipe</handle><handle>pipe1</handle></formats></discovery>""", etree.tostring(utils.dict_to_lxml(root, dictionary)))

    def test_content_type_for_xml(self):
        self.assertEquals('text/xml; charset=utf-8', utils.content_type_for("xml"))

    def test_content_type_for_json(self):
        self.assertEquals('application/json; charset=utf-8', utils.content_type_for("json"))

