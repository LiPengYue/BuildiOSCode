
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom

import iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserStaticStr as IOSXIBDomStaticStr

class iOSXIBConstraintModel:
    nodeElement:xml.dom.minidom.Element
    nodeId: str
    firstItem: str
    firstAttribute: str
    secondItem: str
    secondAttribute: str
    constant: str
    id: str
    priority: str
    symbolic: str

    def __init__(self,nodeElement: xml.dom.minidom.Element,nodeId:str):
        self.nodeId = nodeId
        self.nodeElement = nodeElement
        self.reloadPropertys()

    def reloadPropertys(self):
        if self.nodeElement is None:
            print('self.nodeList: none')
            return

        self.firstItem = self.getDomElementAttribute(IOSXIBDomStaticStr.key_firstItem)
        self.firstAttribute = self.getDomElementAttribute(IOSXIBDomStaticStr.key_firstAttribute)
        self.secondItem = self.getDomElementAttribute(IOSXIBDomStaticStr.key_secondItem)
        self.secondAttribute = self.getDomElementAttribute(IOSXIBDomStaticStr.key_secondAttribute)
        self.constant = self.getDomElementAttribute(IOSXIBDomStaticStr.key_constant)
        self.id = self.getDomElementAttribute(IOSXIBDomStaticStr.key_id)
        self.priority = self.getDomElementAttribute(IOSXIBDomStaticStr.key_priority)
        self.symbolic = self.getDomElementAttribute(IOSXIBDomStaticStr.key_symbolic)

    def getDomElementAttribute(self,key:str):
        return self.getElementAttributeValue(self.nodeElement, key)

    def convertToDict(self) -> dict:
        dic:dict = {}
        dic[IOSXIBDomStaticStr.key_firstItem] = self.firstItem
        dic[IOSXIBDomStaticStr.key_firstAttribute] = self.firstAttribute
        dic[IOSXIBDomStaticStr.key_secondItem] = self.secondItem
        dic[IOSXIBDomStaticStr.key_secondAttribute] = self.secondAttribute
        dic[IOSXIBDomStaticStr.key_constant] = self.constant
        dic[IOSXIBDomStaticStr.key_id] = self.id
        dic[IOSXIBDomStaticStr.key_priority] = self.priority
        dic[IOSXIBDomStaticStr.key_symbolic] = self.symbolic
        return dic

    def getElementAttributeValue(self, element: xml.dom.minidom.Element, key: str) -> xml.dom.minidom.Element:
        if (element is xml.dom.minidom.Element == False):
            return None
        lementValue = element.getAttribute(key)
        if (lementValue is None):
            return None
        return lementValue
