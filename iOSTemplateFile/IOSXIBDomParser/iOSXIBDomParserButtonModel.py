
from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserBaseViewModel import iOSXIBDomParserBaseViewModel as IOSBaseViewModel
import iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserStaticStr  as IDomParserStr
import iOSTemplateFile.IOSCreate.ios_static_string as IStaticStr

class iOSXIBDomParserButtonModel(IOSBaseViewModel):

    fontFamilyName: str = ''
    fontSize: str = '0.0'
    fontFamily: str = ''
    textNormal: str = ''
    textSelected:str = ''
    textColorNormal: str = ''
    textColorSelect: str = ''

    def parseClassTypeProperty(self) -> str:
        return IDomParserStr.key_UIButton

    def subParsePropertys(self):
        # print(self.nodeElement.toxml())
        self.parseFont()
        self.parseText()

    def parseText(self):
        stateElementArray = self.getElements(self.nodeElement,IDomParserStr.key_state)
        for stateElement in stateElementArray:
            state = self.getElementAttributeValue(stateElement,IDomParserStr.key_key)
            text = self.getElementAttributeValue(stateElement,IDomParserStr.key_title)
            colorElement = self.getFirstElement(stateElement, IDomParserStr.key_color)
            color = self.getColorWithElement(colorElement)

            if state == IDomParserStr.key_normal:
                self.textNormal = text
                self.textColorNormal = color

            if state == IDomParserStr.key_selected:
                self.textSelected = text
                self.textColorSelect = color

    def parseFont(self):
        fontElement = self.getFirstElement(self.nodeElement,IDomParserStr.key_fontDescription)
        self.fontFamily = self.getElementAttributeValue(fontElement,IDomParserStr.key_family)
        self.fontFamilyName = self.getElementAttributeValue(fontElement, IDomParserStr.key_name)
        self.fontSize = self.getElementAttributeValue(fontElement,IDomParserStr.key_pointSize)

    def subConvertToDic(self) -> dict:
        jsonDic:dict = {}
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_FontFamily] = self.fontFamily
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_FontFamilyName] = self.fontFamilyName
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_FontSize] = self.fontSize
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_NormalTextKey] = self.textNormal
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_SelectTextKey] = self.textSelected
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_NormalTextColorKey] = self.textColorNormal
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_SelectTextColorKey] = self.textColorSelect
        return jsonDic
