#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom

from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParserViewModel import iOSXIBDomParserViewModel as IOSViewModel
import xml.etree.ElementTree as ET

# <?xml version="1.0"?>
# <data>
#     <country name="Liechtenstein">
#         <rank>1</rank>
#         <year>2008</year>
#         <gdppc>141100</gdppc>
#         <neighbor name="Austria" direction="E"/>
#         <neighbor name="Switzerland" direction="W"/>
#     </country>
#     <country name="Singapore">
#         <rank>4</rank>
#         <year>2011</year>
#         <gdppc>59900</gdppc>
#         <neighbor name="Malaysia" direction="N"/>
#     </country>
#     <country name="Panama">
#         <rank>68</rank>
#         <year>2011</year>
#         <gdppc>13600</gdppc>
#         <neighbor name="Costa Rica" direction="W"/>
#         <neighbor name="Colombia" direction="E"/>
#     </country>
# </data>


class DomParser:

    def parse(self,fileName:str):
        # tree = ET.parse(fileName)
        # root = tree.getroot()
        # # Find all subview elements
        # views = root.findall(".//view")
        # subviews = root.findall(".//subviews/*")
        # # print(views[0].text)
        # # return
        # # Loop through the subviews and print their IDs
        # for subview in subviews:
        #     subview_id = subview.get("id")
        #     print(subview_id)


        #
        #
        #
        #
        # return
        DOMTree = xml.dom.minidom.parse(fileName)
        collection = DOMTree.documentElement

        # print(collection.toxml())
        # return
        if collection.hasAttribute("data"):
            print ("Root element : %s" % collection.getAttribute("data"))

        objects = collection.getElementsByTagName("objects")
        view = objects[0].getElementsByTagName("view")
        print(type(view))
        viewModel = IOSViewModel(nodeElement=view[0])
        subviewNodeList = view[0].getElementsByTagName("subviews")  # subviews: xml.dom.minicompat.NodeList
        return
        subviews:xml.dom.minicompat.NodeList = view[0].getElementsByTagName("subviews")

        for subview in subviews:
            print(type(subview))
            print(subview)

        return;
        #label
        for subview in subviews:
            label:xml.dom.minicompat.NodeList = subview.getElementsByTagName("label")
            print (label[0].getElementsByTagName("color")[0].getAttribute("key"))

        userDefinedRuntimeAttributes:xml.dom.minicompat.NodeList = label[0].getElementsByTagName("userDefinedRuntimeAttributes")
        for userDefinedRuntimeAttributeItem in userDefinedRuntimeAttributes:
            userDefinedRuntimeAttribute = userDefinedRuntimeAttributeItem.getElementsByTagName('userDefinedRuntimeAttribute')

            for subUserDefinedRuntimeAttribute in userDefinedRuntimeAttribute:
                print(type(subUserDefinedRuntimeAttribute))
                print(subUserDefinedRuntimeAttribute.toxml())
                print(subUserDefinedRuntimeAttribute.getAttribute("type"))
                print(subUserDefinedRuntimeAttribute.getAttribute("keyPath"))
                print(subUserDefinedRuntimeAttribute.getAttribute("value"))
                print('\n---------\n')
        # userDefinedRuntimeAttribute = userDefinedRuntimeAttributes[0].getElementsByTagName("userDefinedRuntimeAttribute")
        # result = userDefinedRuntimeAttribute
        # print(type(result))
        # print(result[0].toxml())

        return
        for country in view:
            print ("*****Country*****")
            if country.hasAttribute("name"):
                print ("Name: %s" % country.getAttribute("name"))
            rank = country.getElementsByTagName('rank')[0]
            print ("Rank: %s" % rank.childNodes[0].data)
            year = country.getElementsByTagName('year')[0]
            print ("Year: %s" % year.childNodes[0].data)
            gdppc = country.getElementsByTagName('gdppc')[0]
            print ("Gdppc: %s" % gdppc.childNodes[0].data)
            neighbors = country.getElementsByTagName('neighbor')
            for neighbor in neighbors:
                print ("Neighbor:", neighbor.getAttribute("name"),neighbor.getAttribute("direction"))


if __name__ == '__main__':
    parser=DomParser()
    parser.parse("/Users/lp1/Desktop/XIB/XIB/ZRXIBView.xib")
