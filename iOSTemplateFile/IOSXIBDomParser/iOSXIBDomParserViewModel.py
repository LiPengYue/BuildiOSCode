#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserLabelModel import iOSXIBDomParserLabelModel as IOSLabelModel
from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserButtonModel import iOSXIBDomParserButtonModel as IOSButtonModel
from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserImageViewModel import iOSXIBDomParserImageViewModel as IOSImageViewModel
import iOSTemplateFile.IOSCreate.ios_static_string as IStaticStr
import iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserStaticStr  as IDomParserStr
from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserBaseViewModel import iOSXIBDomParserBaseViewModel as IOSBaseViewModel
import colorsys

import xml.etree.ElementTree as ET

# def parse_xib(file_path):
#     tree = ET.parse(file_path)
#     root = tree.getroot()
#     # Find all subview elements
#     subviews = root.find(".//view/*")
#     print(type(subviews))
#     # Loop through the subviews and print their IDs
#     for subview in subviews:
#         subview_id = subview.get("id")
#         print(subview_id)
#
# import iOSTemplateFile.IOSXIBDomParser.iOSXIBConstraintParser as iOSXIBConstraintParser

class iOSXIBDomParserViewModel(IOSBaseViewModel):
    def reloadProperty(self,
                       name: str,
                       classType:str,
                       id: str,
                       subviews: dict,  # id : iOSXIBDomParserModel
                       backgroundColor: colorsys,  # color
                       borderColor: colorsys,
                       borderWidth: float,
                       cornerRadius: float):
        self.name = name
        self.id = id
        self.subviews = subviews
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.cornerRadius = cornerRadius
        self.classType = classType

    def parseNodeSubviews(self):
        # subviewNodeList = self.nodeElement.getElementsByTagName("subviews")  # subviews: xml.dom.minicompat.NodeList
        subviewNode = self.getFirstElement(self.nodeElement,IDomParserStr.key_subviews)
        if subviewNode is not None:
            # print(subviewNode.toxml())
            childNodeList = subviewNode.childNodes
            # labelNodeList = subviewNode.getElementsByTagName("label") # label: xml.dom.minicompat.NodeList
            for childNode in childNodeList:
                if (childNode.nodeType == 3):  # DOM Text node
                    continue
                # print(childNode.toxml())
                self.createSubviewWithNode(childNode)


        # print(self.subviews)

    def parseNodeElement(self):
      pass


    def createSubviewWithNode(self, childNode:xml.dom.minidom.Element) -> IOSBaseViewModel:
        nodeName = childNode.nodeName
        node:IOSBaseViewModel = None

        if (nodeName ==  IDomParserStr.key_label):
            node = IOSLabelModel(nodeElement=childNode)

        if (nodeName == IDomParserStr.key_view):
            node = iOSXIBDomParserViewModel(nodeElement=childNode)

        if (nodeName == IDomParserStr.key_imageView):
            node = IOSImageViewModel(nodeElement=childNode)

        if (nodeName == IDomParserStr.key_button):
            node = IOSButtonModel(nodeElement=childNode)

        if (node is None):
            # return
            node = iOSXIBDomParserViewModel(nodeElement=childNode)
        childNodeId = node.nodeId

        if (IStaticStr.str_is_empty(childNodeId) is False and node is not None):
            if (self.classType == IDomParserStr.key_UILabel):
                return
            self.subviews[childNodeId] = node

    def getConstrainsJson(self):
        pass

