
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

        "templateViewName": "iOSTemplateBaseView",
        "templateBaseViewName": "BaseView",

        "templateViewModelName": "iOSTemplateViewModel",
        "templateBaseViewModelName": "iOSTemplateBaseViewModel",

        "templateViewPath": "/Users/lp1/Desktop/pythonProject/iOSTemplateFile/iOSTemplate",
        "templateViewModelPath": "/Users/lp1/Desktop/pythonProject/iOSTemplateFile/iOSTemplate",

        "savePath": "/Users/lp1/01我的文件/一些资料/code/2.Client_fork/1. demos/AVPlayer/AVPlayer/Demos/PythonMakeCode"

    }


def config(dic: dict):
    staticRootConfigDic.update(dic)


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
