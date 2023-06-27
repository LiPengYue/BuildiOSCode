staticColorConfigDic = \
    {
        "annotation_NetApiCreateColor": "根据字段创建UIColor对象,'#colorName#' 为字段名",
        "NetApiCreateColor": "[UIColor : colorWithName: #colorName#]",
        "annotation_DefineHexCreateColor": "根据宏定义创建UIColor对象,'#colorName#' 为16进制参数",
        "DefineHexCreateColor": "ColorDefine(#colorName#)",
        "annotation_StaticCreateColorList": "默认宏定义UIColor对象数组,key为宏定义，value为16进制颜色",
        "DefineCreateColorList": {
            "define_red": "0xFFFF0000"
        }
    }

def config(dic: dict):
    staticColorConfigDic.update(dic)

def setColorConfigDic(NetApiCreateColor: str, DefineHexCreateColor: str, DefineCreateColorDic: dict):
    staticColorConfigDic["NetApiCreateColor"] = NetApiCreateColor
    staticColorConfigDic["DefineHexCreateColor"] = DefineHexCreateColor
    staticColorConfigDic["DefineCreateColorList"] = DefineCreateColorDic


def getDefineHexColor(hex: str):
    if '#' in hex:
        hex = '0x' + hex[1:]
    for key, value in staticColorConfigDic["DefineCreateColorList"].items():
        if value == hex:
            return key

    hexDefineColorStr = staticColorConfigDic["DefineHexCreateColor"]
    hexDefineColorStr = hexDefineColorStr.replace("#colorName#", hex)
    return hexDefineColorStr


def getNetAPIColor(hexApiName: str,defaultColorHex:str):
    apiColorStr = staticColorConfigDic["NetApiCreateColor"]
    replaceStr = hexApiName
    if defaultColorHex is not None and isinstance(defaultColorHex,str) and len(defaultColorHex) > 0:
        replaceStr = f'{hexApiName} ?: @"{defaultColorHex}"'
    apiColorStr = apiColorStr.replace("#colorName#", replaceStr)
    return apiColorStr


def getDefineCreateColor(defineColorStr: str):
    DefineCreateColorDic = staticColorConfigDic["DefineCreateColorList"]
    defineColor = DefineCreateColorDic.get(defineColorStr, None)
    return defineColor
