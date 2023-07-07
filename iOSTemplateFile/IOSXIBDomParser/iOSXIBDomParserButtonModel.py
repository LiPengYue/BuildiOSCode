
from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserBaseViewModel import iOSXIBDomParserBaseViewModel as IOSBaseViewModel
import iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserStaticStr  as IDomParserStr
import iOSTemplateFile.IOSCreate.ios_static_string as IStaticStr

class iOSXIBDomParserButtonModel(IOSBaseViewModel):

    fontFamilyName: str = ''
    fontSize: str = 0.0
    fontFamily: str = ''
    text: str = ""

    def parseClassTypeProperty(self) -> str:
        return IDomParserStr.key_UIButton

    def subParsePropertys(self):
        # print(self.nodeElement.toxml())
        self.parseFont()
        self.parseText()

    def parseText(self):
        pass
    def parseFont(self):
        pass

