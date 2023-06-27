import os.path
from iOSTemplateFile.IOSCreate import  ios_static_string as IStatic
import iOSTemplateFile.IOSCreate.confgs.ios_config_color as IConfigColor

def is_static_define_color(color:str) -> bool:
    return IConfigColor.getDefineCreateColor(color) is not None

def is_hex_color(color:str):
    return '#' in color or '0x' in color or '0X' in color

def hex_color_ifneeded(color:str):
    if is_hex_color(color) and '#' in color:
        return color[1:]
    if is_hex_color(color) and '0x' in color or '0x':
        return color[2:]
    return color

def is_net_api_color(color:str):
    color_not_none = IStatic.str_is_not_empty(color)
    return color_not_none and is_static_define_color(color) == False and is_hex_color(color) == False


def convertRGBAToHex(a:int,r:int,g:int,b:int) -> str:
    ll = hex(a)
    hex_r = hex(r)[2:].upper()  # 10进制转16进制，并去掉16进制前面的“0x”，再把得出的结果转为大写
    hex_g = hex(g)[2:].upper()
    hex_b = hex(b)[2:].upper()
    hex_a = hex(a)[2:].upper()
    hex_r0 = hex_r.zfill(2)  # 位数不足2位时补“0”
    hex_g0 = hex_g.zfill(2)
    hex_b0 = hex_b.zfill(2)
    hex_a0 = hex_a.zfill(2)
    hexStr:str = '#' + hex_a0 + hex_r0 + hex_g0 + hex_b0
    return hexStr

def convertHexToRGGA(hex:str) -> ():
    # 分别获得FF，63，47三个十六进制数字
    A16 = hex[0:2]
    R16 = hex[2:4]
    G16 = hex[4:6]
    B16 = hex[6:8]

    # 将十六进制转成十进制
    # 将十进制转成归一化
    a = int(A16,16) / 255.0
    r = int(R16,16) / 255.0
    g = int(G16,16) / 255.0
    b = int(B16,16) / 255.0

    return(a,r,g,b)

class ios_color:

    color_name:str = ''
    datasource_holder:str = ''
    datasource:str = ''
    default_color:str = '0xFAFAFA'

    def __init__(self,color:str,datasource_holder:str='',datasource:str='',default_color:str='0xFAFAFA'):
        self.color_name = color
        self.datasource_holder = datasource_holder
        self.datasource = datasource
        self.default_color = default_color

    def is_net_api_color(self):
        return is_net_api_color(self.color_name)

    def is_empty(self):
        return IStatic.str_is_empty(self.color_name)

    def color(self) -> str:
        color = ''
        if is_static_define_color(self.color_name):
            color = self.color_name
        elif is_hex_color(self.color_name):
            color = IConfigColor.getDefineHexColor(self.color_name)
        elif len(self.datasource_holder) > 0 and len(self.datasource) > 0:
            apiStr = f'{self.datasource_holder}.{self.datasource}.{self.color_name}'
            color = IConfigColor.getNetAPIColor(apiStr,self.default_color).strip()
        return color

