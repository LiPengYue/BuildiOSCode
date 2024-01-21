# -*- mode: python ; coding: utf-8 -*-

import json
import iOSTemplateFile.IOSCreate.ios_class_create as ClasCreate
import iOSTemplateFile.IOSCreate.ios_static_string as IStatic
import iOSTemplateFile.IOSCreate.IOSTemplateRegulars as IOSTemplateRegulars
import iOSTemplateFile.IOSJsonToModel.ios_json_to_model_config as IJsonConfig

_MODEL_PREFIX = "modelNamePrefix"
_MODEL_SUFFIX = "modelNameSuffix"
_ROOT_MODEL_NAME = "rootModelName"
_ROOT_BASE_MODEL_NAME = "baseModelName"
_MODEL_SAVE_PATH = 'modelSavePath'
_MODEL_Data = 'modelData'

_MODEL_COUNTENT_Flig = '_MODEL_COUNTENT_Flig'

_TMEPLATE_MODEL_PATH_H = '/Users/lp1/Desktop/pythonProject/iOSTemplateFile/iOSTemplateModel.h'
_TMEPLATE_MODEL_PATH_M = '/Users/lp1/Desktop/pythonProject/iOSTemplateFile/iOSTemplateModel.m'

_JSON_TO_MODEL_DESCRIPtION = '''
json中需要有：
    {userName}: 用户名(可选)
    {nickName}: 用户昵称（可选）
    {projectName}: 工程名(可选)
    
    {_MODEL_Data}: model中的内容(必传)
    {_MODEL_PREFIX}：表示类名前缀 (可选)
    {_MODEL_SUFFIX}: 表示类名后缀（可选：默认为'Model'）
    {_ROOT_MODEL_NAME}：根model名（可选： 默认为'Root'）
    {_ROOT_BASE_MODEL_NAME}: baseModel名（可选：默认为NSObject）
    {_MODEL_SAVE_PATH}： 存储路径(✅ 必传：在此路径中创建一个Models文件夹，并存在此文件夹下)
'''.format(userName=IStatic.IOS_TEMPLATE_UserName,
           nickName=IStatic.IOS_TEMPLATE_NickName,
           projectName=IStatic.IOS_TEMPLATE_ProjectName,

           _MODEL_Data=_MODEL_Data,
           _MODEL_PREFIX=_MODEL_PREFIX,
           _MODEL_SUFFIX=_MODEL_SUFFIX,
           _ROOT_MODEL_NAME=_ROOT_MODEL_NAME,
           _ROOT_BASE_MODEL_NAME=_ROOT_BASE_MODEL_NAME,
           _MODEL_SAVE_PATH=_MODEL_SAVE_PATH)


def convertMapToModel(json_map: object,
                      prefix: str,
                      model_name: str,
                      suffix: str,
                      superclass_name: str,
                      addProtocol: bool = False) -> [str]:
    sub_result_list = []
    result = ''
    modelName = ClasCreate.getClassNameStr(prefix, model_name, suffix)
    if addProtocol:
        protcol_interface = ClasCreate.getProtocolInterfaceStr(prefix, model_name,
                                                               suffix) + IStatic.IOS_TEMPLATE_char_newline
        result += protcol_interface + result

    class_instens_str = ClasCreate.getClassInterfaceStr(modelName, superclass_name)
    result += class_instens_str

    if isinstance(json_map, dict):
        # 字典类型
        for key, value in json_map.items():
            if IJsonConfig.special(key):
                result += IJsonConfig.special(key)
            elif ClasCreate.isBaseTypeWithValue(value):
                note = ''
                if IStatic.str_is_empty(value) == False:
                    note = f'\n/**{value} */'
                result += note + ClasCreate.getBaseTypePropertyWithTypeValue(value, key)
            else:
                sub_model_name = ClasCreate.camelCase(model_name) + ClasCreate.camelCase(key)
                sub_model_property = ClasCreate.getClassNameStr(prefix, sub_model_name, suffix)
                if isinstance(value, list) == False:
                    result += ClasCreate.getBaseTypePropertyWithTypeValue(value, key, sub_model_property)
                else:
                    result += ClasCreate.getListTypePropertyWithValue(value, key, sub_model_property)

                subvalue: dict = {}
                if isinstance(value, list):
                    subvalue = value[0]

                if isinstance(value, dict):
                    subvalue = value

                if subvalue is None or ClasCreate.isBaseTypeWithValue(subvalue):
                    continue
                sub_result_list += convertMapToModel(subvalue,
                                                     prefix,
                                                     sub_model_name,
                                                     suffix,
                                                     superclass_name,
                                                     addProtocol=isinstance(value, list) == True)

    result += '\n@end\n'

    resultList = []
    resultList.append(result)
    resultList += sub_result_list

    return resultList;


def convertJsonToModel(json_str):
    print('..........' + _JSON_TO_MODEL_DESCRIPtION + '..........')
    json_map = json.loads(json_str)
    json_map = flattenMap(json_map)
    # json_map = removeDuplication(json_map)
    nick_name = json_map.get(IStatic.IOS_TEMPLATE_NickName)
    user_name = json_map.get(IStatic.IOS_TEMPLATE_UserName)
    project_name = json_map.get(IStatic.IOS_TEMPLATE_ProjectName)

    prefix: str = json_map.get(_MODEL_PREFIX, '')
    suffix: str = json_map.get(_MODEL_SUFFIX, 'Model')
    superclass_name: str = json_map.get(_ROOT_BASE_MODEL_NAME, IStatic.IOS_TEMPLATE_TYPE_NSObject)
    root_model_name: str = json_map.get(_ROOT_MODEL_NAME, 'Root')
    model_save_path: str = json_map.get(_MODEL_SAVE_PATH, '') + '/Models'
    if len(model_save_path) == 0:
        print(_JSON_TO_MODEL_DESCRIPtION)
        print('🌶🌶' + _MODEL_SAVE_PATH + '为必传参数')
        return

    result_list = convertMapToModel(json_map=json_map[_MODEL_Data],
                                    prefix=prefix,
                                    model_name=root_model_name,
                                    suffix=suffix,
                                    superclass_name=superclass_name)
    model_h = ''
    for str in result_list:
        model_h += f'\n{str}'

    # protocol
    protocl_tuple = IOSTemplateRegulars.getStrAToStrB(IStatic.IOS_TEMPLATE_Protocol + ' ', '<', model_h)
    protocl_list_content = IStatic.IOS_TEMPLATE_char_newline + IStatic.IOS_TEMPLATE_Protocol
    protocol_tuple_count = len(protocl_tuple)
    for index, value in enumerate(protocl_tuple):
        last = ','
        if index == protocol_tuple_count - 1:
            last = ';\n'
        protocl_list_content += IStatic.IOS_TEMPLATE_char_newline + value + last
    model_h = protocl_list_content + model_h

    # subModel
    model_name_tule = IOSTemplateRegulars.getStrAToStrB(IStatic.IOS_TEMPLATE_Interface + ' ',
                                                        ' ' + IStatic.IOS_TEMPLATE_char_colon, model_h)
    model_name_list_content = IStatic.IOS_TEMPLATE_char_newline * 2 + '@class'
    model_name_tule_count = len(model_name_tule)
    for index, value in enumerate(model_name_tule):
        last = ','
        if index == model_name_tule_count - 1:
            last = ';\n'
        model_name_list_content += IStatic.IOS_TEMPLATE_char_newline + value + last
    model_h = model_name_list_content + model_h

    # 引用
    if superclass_name != IStatic.IOS_TEMPLATE_TYPE_NSObject:
        model_h = IStatic.IOS_TEMPLATE_char_newline + f'#import "{superclass_name}.h' + model_h

    model_h = IStatic.IOS_TEMPLATE_TYPE_Import_UIKit + model_h

    model_m = ClasCreate.getImportFile(ClasCreate.getClassNameStr(prefix, root_model_name, suffix))
    model_m_tup = IOSTemplateRegulars.getStrAToStrB(IStatic.IOS_TEMPLATE_Interface, IStatic.IOS_TEMPLATE_char_colon,
                                                    model_h)
    for model_implementation in model_m_tup:
        model_m += IStatic.IOS_TEMPLATE_Implementation + model_implementation + IStatic.IOS_TEMPLATE_End + IStatic.IOS_TEMPLATE_char_newline

    model_name = ClasCreate.getClassNameStr(prefix, root_model_name, suffix)
    ClasCreate.saveFile(model_h,
                        model_save_path,
                        model_name + '.h',
                        ClasCreate.getFileDesc(project_name=project_name,
                                               user_name=user_name,
                                               nick_name=nick_name,
                                               className=root_model_name))
    ClasCreate.saveFile(model_m,
                        model_save_path,
                        model_name + '.m',
                        ClasCreate.getFileDesc(project_name=project_name,
                                               user_name=user_name,
                                               nick_name=nick_name,
                                               className=root_model_name))


def isBaseTypeWithValue(value):
    return isinstance(value, bool) | isinstance(value, int) | isinstance(value, float) | isinstance(value, str)


def flattenMap(map) -> dict:
    result: dict = {}
    if isinstance(map, list):
        result = mergetList(map)

    if isinstance(map, dict):
        flatten = {}
        for key, value in map.items():
            if (isBaseTypeWithValue(value)) or flatten.get(key) == None:
                flatten[key] = map[key]
                continue
            else:
                merge_map = flattenMap(map)
                flatten = mergeMap(flatten, merge_map)

        result = flatten
    return result


def mergetList(list: list) -> list:
    if len(list) <= 1:
        return list
    result = {}
    for value in list:
        if isBaseTypeWithValue(value):
            continue
        result = mergeMap(result, value)
    if len(result) == 0:
        return list
    return [result]


def mergeMap(map1: dict, map2: dict):
    if map1 is None:
        return map2
    if map2 is None:
        return map1
    if isinstance(map1, list) and isinstance(map2, list):
        l1 = mergetList(map1)
        l2 = mergetList(map2)
        return mergetList(l1 + l2)

    if isinstance(map1, list) and isinstance(map2, dict):
        l: list = map1
        list.append(map2)
        return mergetList(l)

    if isinstance(map1, list) and isBaseTypeWithValue(map2):
        l: list = map1
        list.append(map2)
        return mergetList(l)

    if isinstance(map1, dict) and isinstance(map1, list):
        l: list = map2
        l.append(map1)
        return mergetList(l)

    if isinstance(map1, dict) and isBaseTypeWithValue(map2):
        return map1

    if isBaseTypeWithValue(map1) and isinstance(map2, list):
        l: list = map2
        l.append(map1)
        return mergetList(l)

    if isBaseTypeWithValue(map1) and isBaseTypeWithValue(map1):
        return map1

    result = map1.copy()
    for key, value in map2.items():
        map1_value = map1.get(key)
        if map1_value is not None:
            # 相同key
            if (isBaseTypeWithValue(value)) == False and isBaseTypeWithValue(map1_value):
                result[key] = flattenMap(value)
            elif (isBaseTypeWithValue(value)) and isBaseTypeWithValue(map1_value):
                continue
            else:
                result[key] = mergeMap(value, map1_value)
        else:
            result[key] = value
    result = flattenMap(result)
    return result


# def removeDuplication(map:dict):
#     map

if __name__ == '__main__':
    json_str = input("请输入json串")
    convertJsonToModel(json_str)


def demo():
    map111 = {}
    convertJsonToModel(map111)