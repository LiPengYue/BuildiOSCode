#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os.path
from xml.dom.minidom import parse
import xml.dom.minidom

from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserViewModel import iOSXIBDomParserViewModel as IOSViewModel

class iOSXIBDomParser:
    viewModel: IOSViewModel
    path: str
    def __init__(self,fileName:str):

        if str is None or isinstance(fileName,str) == False or len(fileName) == 0:
            return
        self.path = fileName
        self.parse(fileName)

    def parse(self,fileName:str):
        if str is None or isinstance(fileName, str) == False or len(fileName) == 0:
            print("请输入正确的path")
            return
        DOMTree = xml.dom.minidom.parse(fileName)
        collection = DOMTree.documentElement
        objects = collection.getElementsByTagName("objects")

        view = objects[0].getElementsByTagName("view")

        viewModel = IOSViewModel(nodeElement=view[0])

        self.viewModel = viewModel
        return viewModel

if __name__ == '__main__':

    parser = iOSXIBDomParser("/Users/lp1/Desktop/XIBDemo/XIBDemo/Demo/ZRXIBView.xib")
    print(parser.viewModel.convertToJson())
    parser.parse("/Users/lp1/Desktop/XIB/XIB/ZRXIBView.xib")
