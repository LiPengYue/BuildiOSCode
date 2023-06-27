
from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserBaseViewModel import iOSXIBDomParserBaseViewModel as IOSBaseViewModel
import iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserStaticStr  as IDomParserStr

class iOSXIBDomParserImageViewModel(IOSBaseViewModel):
    def parseClassTypeProperty(self) -> str:
        return IDomParserStr.key_UIImageView