from iOSTemplateFile.IOSCreate import  ios_static_string as IStatic
const_color_list = ['KColor_Ct1_85',
                            'KColor_Ct1_60',
                            'KColor_Ct1_40',
                            'KColor_Ct1_20',
                            'KColor_Ct1_12',
                            'KColor_Ct2',
                            'KColor_Ct2_60',
                            'KColor_Ct3',
                            'KColor_Ct4',
                            'KColor_Ct5',
                            'KColor_Ct6',
                            'KColor_Ct7',
                            'KColor_Ct8',
                            'KColor_Ct10',
                            'KColor_Ct2_85',
                            'KColor_C2',
                            'KColor_C1_03',
                            'KColor_C1_20',
                            'KColor_C4',
                            'KColor_C4_10',
                            'KColor_C4_06',
                            'KColor_C5',
                            'KColor_C3',
                            'KColor_C6',
                            'KColor_C7',
                            'KColor_C7_60',
                            'KColor_C7_10',
                            'KColor_C8',
                            'KColor_C9',
                            'KColor_C10',
                            'KColor_Cl2',
                            'KColor_Cl1_06',
                            'KColor_Cl1_12',
                            'KColor_Cl1_40',
                            'KColor_Cl1_60',
                            'KColor_Cl4_60',
                            'KColor_Cl10',
                            'KColor_C1_85',
                            'KColor_C1_50',
                            'KColor_C1_10']

def is_static_define_color(color:str) -> bool:
    return color in const_color_list

def is_hex_color(color:str):
    return '#' in color or '0x' in color or '0X' in color

def hex_color_ifneeded(color:str):
    if is_hex_color(color) and '#' in color:
        return color[1:]
    return color
def is_net_api_color(color:str):
    color_not_none = IStatic.str_is_empty(color) == False
    # defin =  is_static_define_color(color)
    # hex = is_hex_color(color)
    # print(f'[color_not_none:{color_not_none}, defin：{defin}, hex：{hex}], is_net_api_color:{ color_not_none and is_static_define_color(color) == False and is_hex_color(color) == False}:【{color}】')
    return color_not_none and is_static_define_color(color) == False and is_hex_color(color) == False

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
            color = f'''
            KColorFromRGB({hex_color_ifneeded(self.color_name)})
            '''.strip()

        elif len(self.datasource_holder) > 0 and len(self.datasource) > 0 and is_net_api_color(self.color_name):
            color = f'''
            [UIColor zr_colorAndAlphaWithHexString: {self.datasource_holder}.{self.datasource}.{self.color_name}?:@"{self.default_color}"]
            '''.strip()
        return color

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
