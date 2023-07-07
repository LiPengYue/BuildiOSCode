import json
import os

from iOSTemplateFile.IOSCreate.ios_view_buider import ios_view_buider as IosViewBuilder
from iOSTemplateFile.IOSXIBDomParser.iOSXIBDomParser import iOSXIBDomParser
from iOSTemplateFile.IOSCreate import ios_static_string as IStaticStr
import iOSTemplateFile.IOSCreate.confgs.ios_config_manager as IConfigManager

if __name__ == '__main__':
    '''
    主函数：程序入口
    '''
    # path = input('请输入XIB路径:')
    # path = '/Users/lp1/Desktop/XIBDemo/XIBDemo/Demo/ZRXIBView.xib'
    path = '/Users/lp1/Desktop/XIBDemo/XIBDemo/Demo/BorderColorXIB.xib'
    # 解析xib
    parser = iOSXIBDomParser(path)
    contentDict = parser.viewModel.convertToDic()

    IConfigManager.config()

    contentDict.update(IConfigManager.getViewBuilderConfigDic())

    filename, suffix = os.path.splitext(os.path.basename(path))
    contentDict[IStaticStr.IOS_TEMPLATE_JSON_PropertyTypeKey] = filename

    # print(json.dumps(contentDict))
    IosViewBuilder().createView(contentDict)
