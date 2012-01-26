from lxml import etree

class XML(object):
    def __init__(self, root_element_name):
        self.root_element = etree.Element(root_element_name)

    def __repr__(self):
        return etree.tostring(self.root_element, encoding='utf-8', xml_declaration=True)

    def append(self, tree):
        self.root_element.append(tree.root_element)

    def set_text(self, value):
        self.root_element.text = value

    def append_dict(self, dictionary):
        if not len(dictionary):
            return self
        key, value = dictionary.popitem()
        element = XML(key)
        if isinstance(value, str):
            element.set_text(value)
        if isinstance(value, dict):
            element.append_dict(value)
        if isinstance(value, list):
            for elem in value:
                element.append(element.append_dict(elem))

        self.append(element)
        return self.append_dict(dictionary)


def content_type_for(format):
    return "text/xml; charset=utf-8" if format == 'xml' else "application/json; charset=utf-8"
