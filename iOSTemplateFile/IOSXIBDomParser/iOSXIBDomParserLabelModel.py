
from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserBaseViewModel import iOSXIBDomParserBaseViewModel as IOSBaseViewModel
import iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserStaticStr  as IDomParserStr
import iOSTemplateFile.IOSCreate.ios_static_string as IStaticStr

class iOSXIBDomParserLabelModel(IOSBaseViewModel):

    fontFamilyName: str = ''
    fontSize: str = 0.0
    fontFamily:str = ''

    def parseClassTypeProperty(self) -> str:
        return IDomParserStr.key_UILabel

    def subParsePropertys(self):
        fonts = self.getElements(self.nodeElement,IDomParserStr.key_fontDescription)
        if fonts is None:
            return

        for fontElement in fonts:
            self.fontFamilyName = self.getElementAttributeValue(fontElement,IDomParserStr.key_name)
            self.fontFamily = self.getElementAttributeValue(fontElement,IDomParserStr.key_family)
            self.fontSize = self.getElementAttributeValue(fontElement,IDomParserStr.key_pointSize)
            break 

    def subConvertToDic(self) -> dict:
        jsonDic:dict = {}
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_FontFamily] = self.fontFamily
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_FontFamilyName] = self.fontFamilyName
        jsonDic[IStaticStr.IOS_TEMPLATE_JSON_FontSize] = self.fontSize
        return jsonDic