#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
import xml.dom.minicompat
import colorsys
import iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserStaticStr  as IDomParserStr
import iOSTemplateFile.IOSCreate.ios_static_string as IStaticStr
import iOSTemplateFile.IOSCreate.ios_view_base_data.ios_color as IColor
from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_convert_model import ios_convert_model as IConvertModel
from iOSTemplateFile.IOSXIBDomParser.iOSXIBConstraintModel import iOSXIBConstraintModel as IConstraintModel

class iOSXIBDomParserBaseViewModel:
    nodeElement: xml.dom.minidom.Element

    name:str = ''
    classType:str = ''
    nodeId:str = ''
    subviews: dict # id : iOSXIBDomParserModel
    backgroundColor: str = "" #color
    textColor: str = ""  # color
    borderColor: str = ''
    borderWidth:float = 0
    cornerRadius:float = 0

    userDefinedRuntimeAttributes: [IConvertModel]
    constraints: {str:IConstraintModel}


    def __init__(self,nodeElement: xml.dom.minicompat.NodeList):

        self.nodeElement = nodeElement
        self.resetProperty()
        # print(type(nodeElement))
        self.parseBasePropertys()
        self.parseNodeSubviews()
        self.parseNodeConstrains()
        self.parseNodeElement()


    def resetProperty(self):
        self.name = ''
        self.classType = ''
        self.nodeId = ''
        self.subviews = {}  # id : iOSXIBDomParserModel
        self.backgroundColor = ""  # color
        self.textColor = ""  # color
        self.borderColor = ''
        self.borderWidth = 0
        self.cornerRadius = 0

        self.userDefinedRuntimeAttributes = []
        self.constraints = {}

    def parseBasePropertys(self):
        # id
        self.parseNodeIdProperty()
        #colors
        self.parseColorsProperty()
        #user custom
        self.parseUserDefinedRuntimeAttributesProperty()
        #user custom bordercolor..
        self.parseUserDefinedRuntimeBorderAttributesProperty()
        #user custom class
        self._private_parseClassTypeProperty()

    # setProperty: NodeId
    def parseNodeIdProperty(self):
        nodeId = self.getElementAttributeValue(self.nodeElement, IDomParserStr.key_id)
        if (IStaticStr.str_is_empty(nodeId) == False):
            self.nodeId = nodeId

    # setProperty: colors
    def parseColorsProperty(self):
        colors = self.getElements(self.nodeElement, IDomParserStr.key_color)
        if (colors is not None):
            for colorElement in colors:
                color = self.getColorWithElement(colorElement)
                colorType = self.getElementAttributeValue(colorElement, IDomParserStr.key_key)
                if (colorType == IDomParserStr.key_backgroundColor):
                    self.backgroundColor = color
                if (colorType == IDomParserStr.key_borderColor):
                    self.borderColor = color
                if (colorType == IDomParserStr.key_textColor):
                    self.textColor = color

    # 用户自定义标签
    def parseUserDefinedRuntimeAttributesProperty(self):
        userDefinedRuntimeNodeList: xml.dom.minicompat.NodeList = self.getElements(self.nodeElement, IDomParserStr.key_userDefinedRuntimeAttributes)
        for node in userDefinedRuntimeNodeList:
            # print(node.toxml())
            attributeList = self.getElements(node,IDomParserStr.key_userDefinedRuntimeAttribute)
            for attri in attributeList:
                # print(attri.toxml())
                keyPath = self.getElementAttributeValue(attri,IDomParserStr.key_keyPath)
                value = self.getElementAttributeValue(attri,IDomParserStr.key_value)
                if (IStaticStr.str_is_empty(value)):
                    valueNodeList = self.getElements(attri,IDomParserStr.key_real)
                    for v in valueNodeList:
                        value = self.getElementAttributeValue(v,IDomParserStr.key_value)
                        if (IStaticStr.str_is_empty(value) is False): break
                type = self.getElementAttributeValue(attri,IDomParserStr.key_type)
                convertModel = IConvertModel(keyPath,value,type)
                self.userDefinedRuntimeAttributes.append(convertModel)

    # 从用户自定义标签中提取
    # key_borderColor
    # key_textColor
    # key_borderWidth
    # key_cornerRadius
    def parseUserDefinedRuntimeBorderAttributesProperty(self):
        for model in self.userDefinedRuntimeAttributes:
            key:str = model.keyPath
            if (key == IDomParserStr.key_borderColor):
                self.borderColor = model.value
            if (key == IDomParserStr.key_textColor):
                self.textColor = model.value
            if (key == IDomParserStr.key_borderWidth):
                self.borderWidth = model.value
            if (key == IDomParserStr.key_cornerRadius):
                self.cornerRadius = model.value

    def reloadProperty(self,
                       name: str,
                       classType:str,
                       nodeId: str,
                       subviews: dict,  # id : iOSXIBDomParserModel
                       backgroundColor: colorsys,  # color
                       borderColor: colorsys,
                       borderWidth: float,
                       cornerRadius: float):
        self.name = name
        self.nodeId = nodeId
        self.subviews = subviews
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.cornerRadius = cornerRadius
        self.classType = classType

    def parseNodeSubviews(self):
        pass

    def parseNodeElement(self):
        pass

    def getConstrainsJson(self):
        pass

    def _private_parseClassTypeProperty(self) -> str:
        customeClass = self.getElementAttributeValue(self.nodeElement, IDomParserStr.key_customClass)
        if (IStaticStr.str_is_empty(customeClass)):
            customeClass = self.parseClassTypeProperty()
        self.classType = customeClass

    def parseNodeConstrains(self):
        constraintsArray:xml.dom.minicompat.NodeList = self.getElements(self.nodeElement,IDomParserStr.key_constraints)
        if (constraintsArray is None):
            return
        if self.nodeId == 'iN0-l3-epB':
            print()

        if constraintsArray.length == 0:
            return

        constraintListNode = constraintsArray[-1]

        if constraintListNode is None:
            return

        constraintList = self.getElements(constraintListNode, IDomParserStr.key_constraint)
        for constraint in constraintList:
            constraintModel: IConstraintModel = IConstraintModel(constraint, self.nodeId)
            viewModel: iOSXIBDomParserBaseViewModel = self.subviews.get(constraintModel.firstItem, None)
            if viewModel is None:
                viewModel: iOSXIBDomParserBaseViewModel = self.subviews.get(constraintModel.secondItem, None)
            if (IStaticStr.str_is_empty(constraintModel.id) is True):
                continue
            if (viewModel is None):
                self.constraints[constraintModel.id] = constraintModel
                continue
            viewModel.constraints[constraintModel.id] = constraintModel

    def parseClassTypeProperty(self) -> str:
        return IDomParserStr.key_UIView

    def getElements(self,element: xml.dom.minidom.Element,key:str) -> xml.dom.minicompat.NodeList :
        if (element is xml.dom.minidom.Element == False):
            return None
        elements = element.getElementsByTagName(key)
        if (elements is xml.dom.minicompat.NodeList == False):
            return None
        return elements

    def getFirstElement(self,element: xml.dom.minidom.Element,key:str) -> xml.dom.minidom.Element:
        list = self.getElements(element,key)
        if list.length > 0:
            return list[0]
        return None

    def getElementAttributeValue(self, element: xml.dom.minidom.Element, key: str) -> xml.dom.minidom.Element:
        if (element is xml.dom.minidom.Element == False):
            return None
        lementValue = element.getAttribute(key)
        if (lementValue is None):
            return None
        return lementValue

    def getColorWithElement(self,colorElement) -> str:
        # print(colorElement.toxml())
        red = self.getElementAttributeValue(colorElement, IDomParserStr.key_color_red)
        green = self.getElementAttributeValue(colorElement, IDomParserStr.key_color_green)
        blue = self.getElementAttributeValue(colorElement, IDomParserStr.key_color_blue)
        alpha = self.getElementAttributeValue(colorElement, IDomParserStr.key_color_alpha)
        isError = IStaticStr.str_is_empty(red) or IStaticStr.str_is_empty(green) or IStaticStr.str_is_empty(alpha) or IStaticStr.str_is_empty(blue)

        if (isError): return ""

        a = round(float(alpha) * 250)
        r = round(float(red) * 250)
        g = round(float(green) * 250)
        b = round(float(blue) * 250)

        hexColor:str = IColor.convertRGBAToHex(a,r,g,b)
        return hexColor
