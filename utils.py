from lxml import etree

def dict_to_lxml(root, dictionary):
    if not len(dictionary):
        return root

    key, value = dictionary.popitem()
    element = etree.Element(key)
    if isinstance(value, str):
        element.text = value
    if isinstance(value, dict):
        element = dict_to_lxml(element, value)
    if isinstance(value, list):
        for elem in value:
            element.append(dict_to_lxml(element, elem))

    root.append(element)
    return dict_to_lxml(root, dictionary)

def content_type_for(format):
    return "text/xml; charset=utf-8" if format == 'xml' else "application/json; charset=utf-8"
