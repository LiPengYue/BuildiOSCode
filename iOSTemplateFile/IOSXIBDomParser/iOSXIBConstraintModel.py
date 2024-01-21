
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
import iOSTemplateFile.IOSCreate.ios_static_string as IStaticStr
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
    relation:str # 大于等于、等于、小于等于

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
        self.relation = self.getDomElementAttribute(IOSXIBDomStaticStr.key_relation)
        if (self.firstAttribute == "trailing"):
            self.constant = f'-{self.constant}'


    def getDomElementAttribute(self,key:str):
        return self.getElementAttributeValue(self.nodeElement, key)

    def convertToDict(self) -> dict:
        dic:dict = {}
        dic[IStaticStr.IOS_TEMPLATE_JSON_FirstItem] = self.firstItem
        dic[IStaticStr.IOS_TEMPLATE_JSON_FirstAttribute] = self.firstAttribute
        dic[IStaticStr.IOS_TEMPLATE_JSON_SecondItem] = self.secondItem
        dic[IStaticStr.IOS_TEMPLATE_JSON_SecondAttribute] = self.secondAttribute
        dic[IStaticStr.IOS_TEMPLATE_JSON_Constant] = self.constant
        dic[IStaticStr.IOS_TEMPLATE_JSON_Id] = self.id
        dic[IStaticStr.IOS_TEMPLATE_JSON_Priority] = self.priority
        dic[IStaticStr.IOS_TEMPLATE_JSON_Symbolic] = self.symbolic
        dic[IStaticStr.IOS_TEMPLATE_JSON_Relation] = self.relation
        return dic

    def getElementAttributeValue(self, element: xml.dom.minidom.Element, key: str) -> xml.dom.minidom.Element:
        if (element is xml.dom.minidom.Element == False):
            return None
        lementValue = element.getAttribute(key)
        if (lementValue is None):
            return None
        return lementValue
