
from enum import Enum
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic

class font_family_name(str,Enum):
    Regular = 'PingFangSC-Regular'
    Medium = 'PingFangSC-Medium'
    Light = 'PingFangSC-Light'
    Semibold = 'PingFangSC-Semibold'
    DDinBold = 'D-DIN-Bold'


class ios_font:
    family_name:str
    size:str = ''
    def __init__(self,family_name:str,size:str):
        self.family_name = family_name
        self.size = size

    def kCommonRegularFontOfSize(self):
        return f'kCommonRegularFontOfSize({self.size})'
    def kCommonMediumFontOfSize(self):
        return f'kCommonMediumFontOfSize({self.size})'
    def kCommonLightFontOfSize(self):
        return f'kCommonLightFontOfSize({self.size})'
    def kCommonBoldFontOfSize(self):
        return f'kCommonBoldFontOfSize({self.size})'
    def kDDinBoldFontOfSize(self):
        return f'kDDinBoldFontOfSize({self.size})'
    def is_empty(self) -> bool:
        return IStatic.str_is_empty(self.size) or IStatic.str_is_empty(self.family_name)

    def font(self):
        font = ''
        if self.family_name == font_family_name.Regular:
            font = self.kCommonRegularFontOfSize()
        if self.family_name == font_family_name.Medium:
            font = self.kCommonMediumFontOfSize()
        if self.family_name == font_family_name.Light:
            font = self.kCommonLightFontOfSize()
        if self.family_name == font_family_name.Semibold:
            font = self.kCommonBoldFontOfSize()
        if self.family_name == font_family_name.DDinBold:
            font = self.kDDinBoldFontOfSize()
        if font is None and self.family_name is not None:
            font = f'[UIFont fontWithName:{self.family_name} size:({self.size})]'
        return font