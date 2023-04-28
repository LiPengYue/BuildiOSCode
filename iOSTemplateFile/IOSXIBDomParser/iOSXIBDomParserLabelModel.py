
from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserBaseViewModel import iOSXIBDomParserBaseViewModel as IOSBaseViewModel
import iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserStaticStr  as IDomParserStr
import iOSTemplateFile.IOSCreate.ios_static_string as IStaticStr

class iOSXIBDomParserLabelModel(IOSBaseViewModel):
    def parseClassTypeProperty(self) -> str:
        return IDomParserStr.key_UILabel

