staticFontConfigDic: dict = \
    {
        "annotation_DefineCreateFont": "根据字体名创建UIFont对象,'#FontSize#' 会替换成float类型",
        "DefineCreateFont": {

            "PingFangSC-Regular": "FontPingFangSCR(#fontSize#)",
            "PingFangSC-Medium": "FontPingFangSCM(#fontSize#)",
            "PingFangSC-Light": "FontPingFangSCL(#fontSize#)",
        },
        "annotation_CreateFont": "根据family_name创建UIFont对象,'#familyName#' 为font名, #fontSize#为size",
        "CreateFont": "[UIFont fontWithName:#familyName# size:#fontSize#]",
    }


def config(dic: dict):
    staticFontConfigDic = dic

def getDefineCreateFont(familyName:str) ->str:
    return staticFontConfigDic["DefineCreateFont"].get(familyName,None)

def createFont(familyName:str,size:str) ->str:
    if familyName is None or size is None or len(familyName) == 0 or len(size) == 0:
        return ""
    font = getDefineCreateFont(familyName)
    if font is not None:
        font = font.replace('#fontSize#',size)
    elif staticFontConfigDic["CreateFont"] is not None:
        font = staticFontConfigDic["CreateFont"]
        font = font.replace('#fontSize#',size)
        font = font.replace('#familyName#', f"@\"{familyName}\"")

    if font is None:
        font = ""
    return font
