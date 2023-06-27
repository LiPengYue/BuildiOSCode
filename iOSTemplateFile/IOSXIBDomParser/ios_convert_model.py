#!/usr/bin/python
# -*- coding: UTF-8 -*-
import iOSTemplateFile.IOSCreate.ios_static_string as IStaticStr
class ios_convert_model:
    keyPath:str = ""
    value:str = ""
    type:str = ""

    def __init__(self,keyPath:str, value:str, type:str):
        self.keyPath = keyPath
        self.value = value
        self.type = type

    def convertToDic(self) -> dict:
        dic = {}
        dic[IStaticStr.IOS_TEMPLATE_JSON_UserAttributesKeyPath] = self.keyPath
        dic[IStaticStr.IOS_TEMPLATE_JSON_UserAttributesValue] = self.value
        dic[IStaticStr.IOS_TEMPLATE_JSON_UserAttributesType] = self.type
        return dic