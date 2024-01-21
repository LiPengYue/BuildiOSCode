#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.dom.minicompat
import colorsys
import iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserStaticStr  as IDomParserStr
import iOSTemplateFile.IOSCreate.ios_static_string as IStaticStr
import iOSTemplateFile.IOSCreate.ios_view_base_data.ios_color as IColor
from iOSTemplateFile.IOSXIBDomParser.ios_convert_model import ios_convert_model as IConvertModel
from iOSTemplateFile.IOSXIBDomParser.iOSXIBConstraintModel import iOSXIBConstraintModel as IConstraintModel


class iOSXIBDomParserBaseViewModel:
    nodeElement: xml.dom.minidom.Element

    propertyName: str = ''
    apiName: str = ''
    textAPI: str = ''
    imageAPI: str = ''
    textColorAPI: str = ''
    bgColorAPI: str = ''

    classType: str = ''
    nodeId: str = ''
    subviews: dict  # id : iOSXIBDomParserModel
    backgroundColor: str = ""  # color
    textColor: str = ""  # color
    borderColor: str = ''
    borderWidth: str = 0
    cornerRadius: str = 0

    userDefinedRuntimeAttributes: [IConvertModel]
    constraints: {str: IConstraintModel}

    def __init__(self, nodeElement: xml.dom.minicompat.NodeList):

        self.nodeElement = nodeElement
        self.resetProperty()
        # print(type(nodeElement))
        self.parseBasePropertys()
        self.parseNodeSubviews()
        self.parseNodeConstrains()
        self.parseNodeElement()

    def resetProperty(self):
        self.propertyName = ''
        self.classType = ''
        self.nodeId = ''
        self.subviews = {}  # id : iOSXIBDomParserModel
        self.backgroundColor = ""  # color
        self.textColor = ""  # color
        self.borderColor = ''
        self.borderWidth = '0'
        self.cornerRadius = '0'
        self.masksToBounds: str = '0'
        self.userDefinedRuntimeAttributes: [IConvertModel] = []
        self.constraints: {str: IConstraintModel} = {}
        self.apiName: str = ''
        self.textApi: str = ''
        self.imageAPI: str = ''
        self.textColorApi: str = ''
        self.bgColorAPI: str = ''
        self.fontFamilyName = ''
        self.fontSize = 0

    def parseBasePropertys(self):
        # id
        self.parseNodeIdProperty()
        # colors
        self.parseColorsProperty()
        # user custom
        self.parseUserDefinedRuntimeAttributesProperty()
        # user custom bordercolor..
        self.parseUserDefinedRuntimeBorderAttributesProperty()
        # user maskstobounds
        self.parseMasksToBoundsProperty()
        # user custom class
        self._private_parseClassTypeProperty()
        self.subParsePropertys()

    def subParsePropertys(self):
        pass

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
        userDefinedRuntimeNodeList: xml.dom.minicompat.NodeList = self.getElements(self.nodeElement,
                                                                                   IDomParserStr.key_userDefinedRuntimeAttributes)
        if len(userDefinedRuntimeNodeList) == 0:
            return
        userDefinedRuntimeNodeList = [userDefinedRuntimeNodeList[-1]]
        for node in userDefinedRuntimeNodeList:
            # print(node.toxml())
            attributeList = self.getElements(node, IDomParserStr.key_userDefinedRuntimeAttribute)
            # attributeList = [attributeList[-1]]
            for attri in attributeList:
                # print(attri.toxml())
                keyPath = self.getElementAttributeValue(attri, IDomParserStr.key_keyPath)
                value = self.getElementAttributeValue(attri, IDomParserStr.key_value)
                type = self.getElementAttributeValue(attri, IDomParserStr.key_type)

                if type == IDomParserStr.key_color and IStaticStr.str_is_empty(value):
                    valueNodeList = self.getElements(attri, IDomParserStr.key_color)
                    for v in valueNodeList:
                        value = self.getColorWithElement(v)
                        if (IStaticStr.str_is_empty(value) is False): break

                if (IStaticStr.str_is_empty(value)):
                    valueNodeList = self.getElements(attri, IDomParserStr.key_real)
                    for v in valueNodeList:
                        value = self.getElementAttributeValue(v, IDomParserStr.key_value)
                        if (IStaticStr.str_is_empty(value) is False): break
                type = self.getElementAttributeValue(attri, IDomParserStr.key_type)
                convertModel = IConvertModel(keyPath, value, type)
                self.userDefinedRuntimeAttributes.append(convertModel)
            break

    # 从用户自定义标签中提取
    # key_borderColor
    # key_textColor
    # key_borderWidth
    # key_cornerRadius
    def parseUserDefinedRuntimeBorderAttributesProperty(self):
        for model in self.userDefinedRuntimeAttributes:
            key: str = model.keyPath
            if (key == IDomParserStr.key_borderColor):
                self.borderColor = str(model.value)
            if (key == IDomParserStr.key_textColor):
                self.textColor = str(model.value)
            if (key == IDomParserStr.key_borderWidth):
                self.borderWidth = str(model.value)
            if (key == IDomParserStr.key_cornerRadius):
                self.cornerRadius = str(model.value)
            if (key == IDomParserStr.key_propertyName):
                self.propertyName = str(model.value)
            if (key == IDomParserStr.key_APINameKey):
                self.apiName = str(model.value)
            if (key == IDomParserStr.key_textColorAPI):
                self.textColorAPI = str(model.value)
            if (key == IDomParserStr.key_textAPI):
                self.textAPI = str(model.value)
            if (key == IDomParserStr.key_imageAPI):
                self.imageAPI = str(model.value)
            if (key == IDomParserStr.key_bgColorAPI):
                self.bgColorAPI = str(model.value)

    def parseMasksToBoundsProperty(self):
        str = self.getElementAttributeValue(self.nodeElement, IStaticStr.IOS_TEMPLATE_JSON_MasksToBoundsKey)
        if IStaticStr.str_is_empty(str):
            return
        self.masksToBounds = bool(str)

    def reloadProperty(self,
                       name: str,
                       classType: str,
                       nodeId: str,
                       subviews: dict,  # id : iOSXIBDomParserModel
                       backgroundColor: colorsys,  # color
                       borderColor: colorsys,
                       borderWidth: str,
                       cornerRadius: str):
        self.propertyName = name
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

    def _private_parseClassTypeProperty(self):
        customeClass = self.getElementAttributeValue(self.nodeElement, IDomParserStr.key_customClass)
        if (IStaticStr.str_is_empty(customeClass)):
            customeClass = self.parseClassTypeProperty()
        self.classType = customeClass

    def parseNodeConstrains(self):
        constraintsArray: xml.dom.minicompat.NodeList = self.getElements(self.nodeElement,
                                                                         IDomParserStr.key_constraints)
        if (constraintsArray is None):
            return

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
        nodeName = self.nodeElement.nodeName
        if IStaticStr.str_is_not_empty(nodeName):
            nodeName:str = nodeName.capitalize()
            nodeName = nodeName.replace('view','View')
            nodeName = "UI" + nodeName
            return nodeName
        return IDomParserStr.key_UIView

    def getElements(self, element: xml.dom.minidom.Element, key: str) -> xml.dom.minicompat.NodeList:
        if (element is xml.dom.minidom.Element == False):
            return None
        elements = element.getElementsByTagName(key)
        if (elements is xml.dom.minicompat.NodeList == False):
            return None
        return elements

    def getFirstElement(self, element: xml.dom.minidom.Element, key: str) -> xml.dom.minidom.Element:
        list = self.getElements(element, key)
        if list.length > 0:
            return list[0]
        return None

    def getElementAttributeValue(self, element: xml.dom.minidom.Element, key: str) -> xml.dom.minidom.Element:
        if (element is None):
            return None
        if (element is xml.dom.minidom.Element == False):
            return None
        lementValue = element.getAttribute(key)
        if (lementValue is None):
            return None
        return lementValue

    def getColorWithElement(self, colorElement) -> str:
        # print(colorElement.toxml())
        type = self.getElementAttributeValue(colorElement, IDomParserStr.key_color_type_systemColor)
        if (IStaticStr.str_is_not_empty(type)):
            return IDomParserStr.key_color_type_systemColorPrefix + type

        red = self.getElementAttributeValue(colorElement, IDomParserStr.key_color_red)
        green = self.getElementAttributeValue(colorElement, IDomParserStr.key_color_green)
        blue = self.getElementAttributeValue(colorElement, IDomParserStr.key_color_blue)
        white = self.getElementAttributeValue(colorElement, IDomParserStr.key_color_white)
        alpha = self.getElementAttributeValue(colorElement, IDomParserStr.key_color_alpha)
        colorSpace = self.getElementAttributeValue(colorElement, IDomParserStr.key_color_colorSpace)

        isError = IStaticStr.str_is_empty(red) or IStaticStr.str_is_empty(green) or IStaticStr.str_is_empty(
            alpha) or IStaticStr.str_is_empty(blue)

        if (isError and colorSpace == IDomParserStr.key_color_colorSpace_custom and IStaticStr.str_is_not_empty(white)):
            red = white
            green = white
            blue = white
            isError = False

        if (isError): return ""

        a = round(float(alpha) * 255)
        r = round(float(red) * 255)
        g = round(float(green) * 255)
        b = round(float(blue) * 255)

        hexColor: str = IColor.convertRGBAToHex(a, r, g, b)
        return hexColor

    def convertToJson(self) -> str:
        jsonStr = json.dumps(self.convertToDic())
        return jsonStr

    def convertToDic(self) -> dict:
        jsonDic = {}

        userDefinedRuntimeAttributes: [IConvertModel]
        constraints: {str: IConstraintModel}
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_PropertyNameKey] = self.propertyName
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_PropertyTypeKey] = self.classType
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_NodeId] = self.nodeId
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_BorderColorKey] = self.borderColor
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_BorderWidthKey] = self.borderWidth
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_BackgroundColorKey] = self.backgroundColor
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_CornerRadiusKey] = self.cornerRadius
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_MasksToBoundsKey] = self.masksToBounds
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_Constraints] = self.convertConstraintsToDic()
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_SubViewsKey] = self.convertSubviewsToDic()
        jsonDic[
            IStaticStr.IOS_TEMPLATE_JSON_UserDefinedRuntimeAttributes] = self.converUserDefinedRuntimeAttributesToDic()
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_NormalTextColorKey] = self.textColor

        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_APINameKey] = self.apiName
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_bgColorAPI] = self.bgColorAPI
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_textColorAPI] = self.textColorAPI
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_textAPI] = self.textAPI
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_imageAPI] = self.imageAPI

        jsonDic.update(self.subConvertToDic())
        return jsonDic

    def subConvertToDic(self) -> dict:
        return {}

    def convertConstraintsToDic(self) -> dict:
        constraintDic = {}
        for key, constraint in self.constraints.items():
            dic = constraint.convertToDict()
            constraintDic[key] = dic
        return constraintDic

    def convertSubviewsToDic(self) -> dict:
        subviewDic = {}
        for key, subview in self.subviews.items():
            if not isinstance(subview, iOSXIBDomParserBaseViewModel):
                continue
            subviewModel: iOSXIBDomParserBaseViewModel = subview
            subviewDic[key] = subviewModel.convertToDic()
        return subviewDic

    def converUserDefinedRuntimeAttributesToDic(self) -> dict:
        arr = []
        for attri in self.userDefinedRuntimeAttributes:
            dic = attri.convertToDic()
            arr.append(dic)
        return arr
