"""XML 파싱 Helper."""

from xml.etree import cElementTree as ElementTree

import requests


class XmlListConfig(list):
    """Xml 을 List 로 가져옴."""

    def __init__(self, a_list):
        super().__init__()
        for element in a_list:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    """
    Example usage.

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> xml_string = "<test>Hello World</test>"
    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    """

    def __init__(self, parent_element):
        """
        초기화.

        :param parent_element:
        """
        super().__init__()
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    a_dict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    a_dict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    a_dict.update(dict(element.items()))
                self.update({element.tag: a_dict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                if element.tag not in self:
                    self.update({element.tag: dict(element.items())})
                elif isinstance(self[element.tag], list):
                    self[element.tag].append(dict(element.items()))
                else:
                    # it was dictionary but it is changed to list
                    new_list = [self[element.tag], dict(element.items())]
                    self[element.tag] = new_list

            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


def get_xml_request(url: str):
    """
    XML 을 리턴하는 URL 을 받아서 파싱된 결과를 리턴.

    :param url: API URL
    :return:
    """
    result = requests.post(url).text.strip()
    tree = ElementTree.ElementTree(ElementTree.fromstring(result))

    return result, tree
