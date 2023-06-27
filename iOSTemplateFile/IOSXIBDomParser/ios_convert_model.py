#!/usr/bin/python
# -*- coding: UTF-8 -*-

class ios_convert_model:
    keyPath:str = ""
    value:str = ""
    type:str = ""

    def __init__(self,keyPath:str, value:str, type:str):
        self.keyPath = keyPath
        self.value = value
        self.type = type
