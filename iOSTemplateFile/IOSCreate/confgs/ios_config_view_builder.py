
from iOSTemplateFile.IOSCreate import ios_static_string as IStaticStr
import json
import os

staticRootConfigDic = \
    {
        "template_projectNameKey": "生成View",
        "template_userNameKey": "李鹏跃",
        "template_nickNameKey": "lpy",

        "baseViewModelName": "LPYBaseViewModel",
        "dataSouceName": "viewModel",

        "templateViewName": "iOSTemplateTableViewCell",
        "templateBaseViewName": "ZRRentBaseTableViewCell",

        "templateViewModelName": "iOSTemplateViewModel",
        "templateBaseViewModelName": "iOSTemplateBaseViewModel",

        "templateViewPath": "/Users/lp1/Desktop/pythonProject/iOSTemplateFile/iOSTemplate",
        "templateViewModelPath": "/Users/lp1/Desktop/pythonProject/iOSTemplateFile/iOSTemplate",

        "savePath": "/Users/lp1/01我的文件/一些资料/code/2.Client_fork/1. demos/AVPlayer/AVPlayer/Demos/PythonMakeCode"

    }


def config(dic: dict):
    for key,value in dic.items():
        staticRootConfigDic[key] = value

def setStaticRootConfigDic(
        template_projectNameKey: str,
        template_userNameKey: str,
        template_nickNameKey: str,
        baseViewModelName: str,
        templateViewName: str,
        templateBaseViewName: str,
        templateViewModelName: str,
        templateBaseViewModelName: str,
        templateViewPath: str,
        templateViewModelPath: str,
        savePath: str,
        dataSouceName: str = "viewModel", ):
    staticRootConfigDic["template_projectNameKey"] = template_projectNameKey
    staticRootConfigDic["template_userNameKey"] = template_userNameKey
    staticRootConfigDic["template_nickNameKey"] = template_nickNameKey

    staticRootConfigDic["baseViewModelName"] = baseViewModelName
    staticRootConfigDic["dataSouceName"] = dataSouceName

    staticRootConfigDic["templateViewName"] = templateViewName
    staticRootConfigDic["templateBaseViewName"] = templateBaseViewName

    staticRootConfigDic["templateViewModelName"] = templateViewModelName
    staticRootConfigDic["templateBaseViewModelName"] = templateBaseViewModelName

    staticRootConfigDic["templateViewPath"] = templateViewPath
    staticRootConfigDic["templateViewModelPath"] = templateViewModelPath

    staticRootConfigDic["savePath"] = savePath


def get_template_projectNameKey():
    return staticRootConfigDic.get("template_projectNameKey", None)


def get_template_userNameKey():
    return staticRootConfigDic.get("template_userNameKey", None)


def get_template_nickNameKey():
    return staticRootConfigDic.get("template_nickNameKey", None)


def get_baseViewModelName():
    return staticRootConfigDic.get("baseViewModelName", None)


def get_dataSouceName():
    return staticRootConfigDic.get("dataSouceName", None)


def get_templateViewName():
    return staticRootConfigDic.get("templateViewName", None)


def get_templateBaseViewName():
    return staticRootConfigDic.get("templateBaseViewName", None)


def get_templateViewModelName():
    return staticRootConfigDic.get("templateViewModelName", None)


def get_templateBaseViewModelName():
    return staticRootConfigDic.get("templateBaseViewModelName", None)


def get_templateViewPath():
    return staticRootConfigDic.get("templateViewPath", None)


def get_templateViewModelPath():
    return staticRootConfigDic.get("templateViewModelPath", None)


def get_savePath():
    return staticRootConfigDic.get("savePath", None)
