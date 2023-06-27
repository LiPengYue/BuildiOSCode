import json
import os
from iOSTemplateFile.IOSCreate import ios_static_string as IStaticStr
import iOSTemplateFile.IOSCreate.confgs.ios_config_view_builder as IConfigView
import iOSTemplateFile.IOSCreate.confgs.ios_config_font as IConfigFont
import iOSTemplateFile.IOSCreate.confgs.ios_config_color as IConfigColor

__rootConfigDefaultStr = '''         
     {
         "template_userNameKey": "名称",
         "template_nickNameKey": "昵称",

         "baseViewModelName": "viewModel的父类",
         "dataSouceName": "view持有的ViewModel属性名",

         "templateViewName": "模板View名",
         "templateBaseViewName": "模板view父类名",

         "templateViewModelName": "模板ViewModel名",
         "templateBaseViewModelName": "模板ViewModel父类名",

         "templateViewPath": "模板view的路径",
         "templateViewModelPath": "模板ViewModel路径",

         "savePath": "生成的代码存储路径"

     }
 '''

__colorConfigDefaultStr = '''
 {
     "annotation_NetApiCreateColor": "根据字段创建UIColor对象,'#colorName#' 为字段名",
     "NetApiCreateColor":"[UIColor : colorWithName: #colorName#]",
     "annotation_DefineHexCreateColor": "根据宏定义创建UIColor对象,'#colorName#' 为16进制参数",
     "DefineHexCreateColor":"ColorDefine(#colorName#)",
     "annotation_StaticCreateColorList": "默认宏定义UIColor对象数组,key为宏定义，value为16进制颜色",
     "DefineCreateColorList": [
         "define_red":"0xFFFF0000"
     ]
 }
 '''

__fontConfigDefaultStr = '''
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
 '''


def __readPath(path: str) -> str:
    result: str = ''
    if IStaticStr.str_is_empty(path):
        print("path不能为空")
        return result
    if os.path.isfile(path) == False:
        print(f"path不是文件目录：{path}")
        return result

    with open(path, encoding='utf-8') as config:
        # 读取文件
        result = config.read()
        result = result.replace('\n', '')
    return result


def __write(path: str, content: str):
    with open(path, 'w') as f:
        f.write(content)
        f.close()


def __writeConfigFilePath(configPath: str):
    configFilePath = IStaticStr.getOtherPath("/ios_config_file_path")
    __write(configFilePath, configPath)


def __readConfiFileDicPath() -> str:
    configFilePath = IStaticStr.getOtherPath("/ios_config_file_path")
    path: str = __readPath(configFilePath)
    return path


def __openFileIfNeeded(path: str, defaultText: str):
    if os.path.exists(path) == False:
        __write(path, defaultText)
    __openFileWithTextEditor(path)

def __openFileWithTextEditor(path: str):
    start = f"\"{path}\""
    os.system(f"open {start}")

def __createConfigDic():
    configFileDicPath = __readConfiFileDicPath()
    if os.path.exists(configFileDicPath) is False:
        if IStaticStr.str_is_empty(configFileDicPath):
            configFileDicPath = input('请输入配置文件（view、color、font）所属文件夹路径')
        __writeConfigFilePath(configFileDicPath)

    if os.path.exists(configFileDicPath) is False:
        os.makedirs(configFileDicPath)

    rootConfigPath = configFileDicPath + '/rootConfig.txt'
    colorConfiPath = configFileDicPath + '/colorConfig.txt'
    fontConfigPath = configFileDicPath + '/fontConfig.txt'

    __openFileIfNeeded(rootConfigPath, __rootConfigDefaultStr)
    __openFileIfNeeded(colorConfiPath, __colorConfigDefaultStr)
    __openFileIfNeeded(fontConfigPath, __colorConfigDefaultStr)

    input('请编辑对应的配置文件（view、color、font），完成请回车\n')

    IConfigView.config(__readConfigDic(rootConfigPath))
    IConfigColor.config(__readConfigDic(colorConfiPath))
    IConfigFont.config(__readConfigDic(fontConfigPath))


def __readConfigDic(path: str) -> dict:
    configPath = path
    dic = {}
    with open(configPath, encoding='utf-8') as config:
        # 读取文件
        contents = config.read()
        contents = contents.replace('\n', '')
        dic = json.loads(contents)
    return dic


def config():
    # 头文件扩展
    __createConfigDic()

def getViewBuilderConfigDic() -> dict:
    return IConfigView.staticRootConfigDic