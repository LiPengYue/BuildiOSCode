from iOSTemplateFile.IOSCreate import ios_static_string as IStatic
import iOSTemplateFile.IOSCreate.confgs.ios_config_font as IConfigFont
class ios_font:
    familyName:str = ''
    family:str = ''
    size:str = ''
    createFontStr:str = ''
    def __init__(self,faimliy:str,familyName:str,size:str):
        self.familyName = familyName
        self.family = faimliy
        self.size = size
        self.createFontStr = self.font()

    def is_empty(self) -> bool:
        return IStatic.str_is_empty(self.familyName) or IStatic.str_is_empty(self.size)

    def font(self):
        if self.is_empty():
            return ''
        font = IConfigFont.createFont(self.familyName,self.size)
        return font