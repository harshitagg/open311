from lxml import etree
import unittest
from discovery import dict_to_lxml


class UtilTests(unittest.TestCase):
    
    def test_dict_to_xml(self):
        dictionary = {'foo':'bar', 'changeset':'2011-12-12','endpoints': {
            'specification':'wewew', 'type':'production'
        }, 'formats':[{'handle': 'pipe'}, {'handle': 'pipe1'}]}
        root = etree.Element('discovery')
        self.assertEquals("""<discovery><changeset>2011-12-12</changeset><foo>bar</foo><endpoints><specification>wewew</specification><type>production</type></endpoints><formats><handle>pipe</handle><handle>pipe1</handle></formats></discovery>""", etree.tostring(dict_to_lxml(root, dictionary)))
