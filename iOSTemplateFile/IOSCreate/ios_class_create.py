# 导入模块
import os
import socket
import datetime
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic
from iOSTemplateFile.IOSCreate import ios_code_style as IStyle

#字符串转成驼峰
def camelCase(string:str,removeNearRepeatWord:bool=True):
    result = ''
    if len(string) > 0:
        string = string.replace("_"," ")
        list = string.split(" ")
        for s in list:
            if IStatic.str_is_empty(s) == False :
                if s in result:
                    continue
                result += s[0].upper() + s[1:]
    segment_list:[str] = []
    segment_str = ''
    for char in result:
        if char.isupper():
            segment_list.append(segment_str)
            segment_str = ''
        segment_str += char
    segment_list.append(segment_str)
    if removeNearRepeatWord == False:
        return ''.join(segment_list)

    result_str = ''
    for i, value in enumerate(segment_list):
        if i == 0:
            result_str = value
            continue
        front:str = segment_list[i-1]
        if front == value and len(front) > 1:
            continue
        result_str += value
    return result_str

# def append_and_camel(left:str,right:str) -> str:


def getFileDescForMap(map,class_name:str=''):
    nick_name = map.get(IStatic.IOS_TEMPLATE_NickName, '')
    user_name = map.get(IStatic.IOS_TEMPLATE_UserName, '')
    project_name = map.get(IStatic.IOS_TEMPLATE_ProjectName, '')
    return getFileDesc(project_name,user_name,nick_name,class_name)

#获取顶部字符
def getFileDesc(project_name='',user_name='',nick_name='',className=''):
    if len(nick_name) == 0:
        nick_name = user_name

    today = datetime.datetime.today()
    year = today.year
    time = f'{year}/{today.month}/{today.day}'

    desc = '''//
//  {className}
//  {project_name}
//  Created by {name} on {time}.
//  Copyright © {year} {nickName}. All rights reserved.
//  '''.format(className = className, project_name = project_name,name = user_name,nickName=nick_name, time = time, year = year)
    return desc

#获取import
def getImportFile(fileName):
    return IStatic.IOS_TEMPLATE_TYPE_Import + f' "{fileName}.h"\n\n'

#获取协议interface
def getProtocolInterfaceStr(preffix,protocolName,suffix,super_protocol_name:str = 'NSObject'):
    return f'{IStatic.IOS_TEMPLATE_Protocol} {getClassNameStr(preffix,protocolName,suffix)}<{super_protocol_name}> @end'

#获取类名
def getClassNameStr(preffix,name,suffix):
    return camelCase(preffix) + camelCase(name) + camelCase(suffix)

#获取类实现行
def getClassInterfaceStr(name,superclass_name='NSObject'):
    return  IStatic.IOS_TEMPLATE_Interface + ' ' + 	camelCase(name) + ' ' + IStatic.IOS_TEMPLATE_char_colon + ' '+ superclass_name

#根据基本类型返回对应的property (如果是string，则把custom_class 定义为代理)
def getBaseTypePropertyWithTypeValue(property_value:object,property_name,custom_class:str='') -> str:
    result = IStatic.IOS_TEMPLATE_char_newline + getPropertyWithValue(property_value,property_name,custom_class) + ';'
    return result

def getPropertyWithValue(property_value,property_name:str,default):
    property_type = ''
    if (len(default) > 0):
        property_type = IStatic.IOS_TEMPLATE_PROPERTY_strong + f' {default} *'

    if isinstance(property_value, str):
        property_type = IStatic.IOS_TEMPLATE_PROPERTY_copy + ' ' + IStatic.IOS_TEMPLATE_TYPE_NSString + ' *'

    if isinstance(property_value, float):
        property_type = IStatic.IOS_TEMPLATE_PROPERTY_assign + ' ' + IStatic.IOS_TEMPLATE_TYPE_CGFloat + ' '

    if isinstance(property_value, bool):
        property_type = IStatic.IOS_TEMPLATE_PROPERTY_assign + ' ' + IStatic.IOS_TEMPLATE_TYPE_BOOL + ' '

    if isinstance(property_value, int):
        property_type = IStatic.IOS_TEMPLATE_PROPERTY_assign + ' ' + IStatic.IOS_TEMPLATE_TYPE_NSInteger + ' '

    return property_type + property_name

def getListTypePropertyWithValue(property_value:list,property_name:str,protocol_name:str='') -> str:
    result = ''
    isList = isinstance(property_value,list)
    if isList == False:
        return ''

    property_type = IStatic.IOS_TEMPLATE_TYPE_NSArray + " *"
    property_prefix = IStatic.IOS_TEMPLATE_PROPERTY_copy

    if len(property_value) > 0:
        item = property_value[0]
        if (len(protocol_name) > 0):
            property_type = IStatic.IOS_TEMPLATE_TYPE_NSArray + f'<{protocol_name}> *'

        if isinstance(item, str):
            property_type = IStatic.IOS_TEMPLATE_TYPE_NSArray  + '<NSString *> *'

        if isinstance(item, float) | isinstance(item, bool) | isinstance(item, int):
            property_type = IStatic.IOS_TEMPLATE_TYPE_NSArray + ' *'

    result = '' + IStatic.IOS_TEMPLATE_char_newline  + property_prefix + ' ' + property_type + property_name + ';'
    return result

def isBaseTypeWithValue(value):
    return isinstance(value, bool) | isinstance(value, int) | isinstance(value, float) | isinstance(value, str)

def saveFile(content, path, filename,content_desc = '',format:bool=True):
    '''
    功能：将文章内容 content 保存到本地文件中
    参数：要保存的内容，路径，文件名
    '''
    # 如果没有该文件夹，则自动生成
    if not os.path.exists(path):
        os.makedirs(path)
        print("已经创建文件目录" + path)
    # 保存文件
    filePath = path + '/' + filename
    with open(filePath, 'w', encoding='utf-8') as f:
        content = content_desc + '\n\n' + content
        f.write(content)
        print("存储成功:"+filePath)
    if format:
        IStyle.format(filePath)