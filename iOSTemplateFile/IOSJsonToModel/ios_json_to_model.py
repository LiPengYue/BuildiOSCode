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
    # json_str = input("请输入json串")
    json_str_array = '''
{
    "modelNameSuffix":"Model",
    "modelNamePrefix":"Rent",
    "template_projectNameKey":"json转model",
    "template_userNameKey":"李鹏跃",
    "template_nickNameKey":"lpy",
    "rootModelName":"filter",
    "baseModelName":"BaseModel",
    "modelSavePath":"/Users/lp1/Desktop/pythonProject/iOSTemplateFile",
    "modelData":{
  "data": {
    "pass_through": "",
    "experiments": {
      "RankOpt": "rankOpt4",
      "searchResblock": ""
    },
    "re_call_type": "",
    "title": "附近房源",
    "rooms": [
      {
        "pic_experiment_id": "listUI",
        "anti_theft_price": [
          "//webimg.ziroom.com/13042b00-831f-4f47-938a-3c819385b6fb.png",
          [
            8,
            4,
            6,
            4
          ]
        ],
        "area_order": 17.7,
        "code": "BJGY0818201537_01",
        "inv_id": "480164",
        "photo_min_webp": "https://img.ziroom.com/pic/static/images/slist_1207/defaultPZZ/natie-loading.jpg_C_240_180_Q100.webp",
        "pic_group_id": "_cross_left",
        "stock_status": "402",
        "ziroom_version_id": 1008,
        "location_id": 1,
        "house_type": 1,
        "apartment_type": 1,
        "district_name": "丰台",
        "price_unit": "/月",
        "type": 1,
        "can_sign_date": 1593532800,
        "lat": 39.846371,
        "subway_station_info": "房源距首经贸站步行约548米",
        "photo_webp": "https://img.ziroom.com/pic/static/images/slist_1207/defaultPZZ/natie-loading.jpg_C_240_180_Q100.webp",
        "floor_total": "14",
        "house_id": "60190013",
        "id": "61180578",
        "is_ai_lock": 1,
        "source": "search#vacancy",
        "style_tag": "朝南",
        "experimentId": "RankOpt",
        "area": "17.7",
        "resblock_name": "万年花城三期",
        "zrrefer": "1602629936451825664|1|1|32.552444|search_result|",
        "photo": "https://img.ziroom.com/pic/static/images/slist_1207/defaultPZZ/natie-loading.jpg_C_240_180_Q100.jpg",
        "session_id": "1602629936451825664",
        "house_code": "BJZRGY0818201537",
        "resblock_id": "1111027380387",
        "tags": [
          {
            "style": {},
            "title": "独立卫生间"
          },
          {
            "title": "可短签"
          },
          {
            "title": "可租1年以上"
          }
        ],
        "parlor": 1,
        "type_text": "合租",
        "city_code": 110000,
        "template_type": 15,
        "can_sign_time": 1561341600,
        "floor": "7",
        "photo_min": "https://img.ziroom.com/pic/static/images/slist_1207/defaultPZZ/natie-loading.jpg_C_240_180_Q100.jpg",
        "bedroom": 3,
        "face": "南",
        "version_name": "1008",
        "air_qualified": 1,
        "bizcircle_name": "玉泉营",
        "inv_no": "746575908",
        "groupId": "rankOpt4",
        "can_sign_short": 1,
        "lng": 116.329405,
        "name": "万年花城三期3居室-南卧",
        "price": 4090,
        "price_style": {
          "color": "#FFFF961E"
        }
      },
      {
        "area_order": 62,
        "template_type": 15,
        "session_id": "1602629936451825664",
        "inv_id": "755572",
        "resblock_id": "1111027377509",
        "tags": [
          {
            "style": {},
            "title": "独立阳台"
          },
          {
            "title": "可短签"
          }
        ],
        "location_id": 2,
        "experimentId": "RankOpt",
        "can_sign_short": 1,
        "source": "search",
        "floor": "4",
        "floor_total": "6",
        "is_ai_lock": 1,
        "price": 6190,
        "sale_status": 3,
        "subway_station_info": "房源距角门西站步行约620米",
        "anti_theft_price": [
          "//webimg.ziroom.com/13042b00-831f-4f47-938a-3c819385b6fb.png",
          [
            1,
            7,
            6,
            4
          ]
        ],
        "area": "62",
        "parlor": 1,
        "house_code": "BJZRGZ1119350098",
        "can_sign_time": 1647401187,
        "photo_min_webp": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.webp",
        "can_sign_date": 1653580800,
        "name": "嘉园二里2居室-南卧",
        "resblock_name": "嘉园二里",
        "id": "62048173",
        "price_unit": "/月",
        "code": "BJZRGZ1119350098_01",
        "price_style": {
          "color": "#FFFF961E"
        },
        "lat": 39.854229,
        "photo": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.jpg",
        "pic_experiment_id": "listUI",
        "ziroom_version_id": 1030,
        "zrrefer": "1602629936451825664|1|2|0.4574888110574212|search_result|",
        "inv_no": "773290484",
        "style_tag": "朝南",
        "air_quality": 2,
        "house_type": 1,
        "pic_group_id": "_cross_left",
        "stock_status": "201",
        "type_text": "合租",
        "bizcircle_name": "马家堡",
        "air_qualified": 1,
        "apartment_type": 1,
        "bedroom": 2,
        "photo_min": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.jpg",
        "groupId": "rankOpt4",
        "version_name": "1030",
        "face": "南",
        "house_id": "60323348",
        "lng": 116.374708,
        "photo_webp": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.webp",
        "type": 1,
        "city_code": 110000,
        "district_name": "丰台"
      },
      {
        "tags": [
          {
            "title": "待释放",
            "style": {
              "background": "#FF7B93B0",
              "color": "#FFFFFFFF"
            }
          },
          {
            "style": {},
            "title": "新小区"
          }
        ],
        "district_name": "朝阳",
        "is_ai_lock": 1,
        "name": "中海城圣朝菲4居室-北卧",
        "area": "23.6",
        "floor": "4",
        "lat": 39.845158,
        "version_name": "1008",
        "code": "BJZRGY0818217066_02",
        "id": "61271593",
        "city_code": 110000,
        "house_id": "60204264",
        "inv_no": "746266478",
        "house_type": 1,
        "pic_group_id": "_cross_left",
        "sale_status": 4,
        "bedroom": 4,
        "bizcircle_name": "成寿寺",
        "lng": 116.458792,
        "groupId": "rankOpt4",
        "can_sign_long": 1,
        "photo_min_webp": "https://img.ziroom.com/pic/static/images/slist_1207/buding-up.jpg_C_240_180_Q100.webp",
        "type": 1,
        "type_text": "合租",
        "anti_theft_price": [
          "//webimg.ziroom.com/13042b00-831f-4f47-938a-3c819385b6fb.png",
          [
            3,
            0,
            6,
            4
          ]
        ],
        "zrrefer": "1602629936451825664|1|3|0.4070836966628289|search_result|",
        "area_order": 23.6,
        "apartment_type": 1,
        "inv_id": "476974",
        "air_qualified": 1,
        "photo": "https://img.ziroom.com/pic/static/images/slist_1207/buding-up.jpg_C_240_180_Q100.jpg",
        "stock_status": "202",
        "subway_station_info": "房源距肖村站步行约1007米",
        "location_id": 3,
        "experimentId": "RankOpt",
        "style_tag": "朝北",
        "price_style": {
          "color": "#FFFF961E"
        },
        "house_code": "BJZRGY0818217066",
        "resblock_id": "1111027382458",
        "face": "北",
        "parlor": 1,
        "photo_webp": "https://img.ziroom.com/pic/static/images/slist_1207/buding-up.jpg_C_240_180_Q100.webp",
        "source": "search",
        "activity_marks": [
          "twoHundredMillion"
        ],
        "can_sign_date": 1603814400,
        "price": 2890,
        "price_unit": "/月",
        "resblock_name": "中海城圣朝菲",
        "session_id": "1602629936451825664",
        "floor_total": "8",
        "photo_min": "https://img.ziroom.com/pic/static/images/slist_1207/buding-up.jpg_C_240_180_Q100.jpg",
        "pic_experiment_id": "listUI",
        "ziroom_version_id": 1008,
        "template_type": 15,
        "can_sign_time": 1561255200,
        "sale_img": "https://image.ziroom.com/g2m1/M00/85/95/ChAFBlvugreAdUurAAAIJIioF8Q667.png"
      },
      {
        "groupId": "rankOpt4",
        "session_id": "1602629936451825664",
        "card_type": "zra",
        "zra_aggs": {
          "rooms": [
            {
              "location_id": 0,
              "price": 66,
              "zrrefer": "",
              "template_type": 1,
              "tags": [
                {
                  "style": {
                    "background": "#1AFF961E",
                    "color": "#FFFF961E"
                  },
                  "hot": 1,
                  "title": "自如寓"
                }
              ],
              "zra_extra": {
                "house_type_name": "虾米即将开业0809",
                "project_name": "虾米prime",
                "rent_unit": "整租1居",
                "rent_unit_type": 2,
                "rooms_count": -1,
                "house_type_id": "8a7693d38280ae010182815ccb9600fa",
                "key_points": "整租1居 | 多种朝向",
                "project_id": "8a768d8b8183f13b018183f36ba40004",
                "reserve_num": -1,
                "zra_display_type": 1
              },
              "name": "虾米即将开业0809·多朝向",
              "subway_station_info": "房源距褡裢坡站步行约3866米",
              "zraExperimentId": "zrasearchstyle",
              "version_name": "10001011",
              "zraGroupId": "doublestyle",
              "area": "1",
              "photo": "http://10.16.34.44:8000/minsu/group3/M00/1A/45/ChAiKmL0z0iAHMiYAACAzxhfS3g611.jpg_Z_930_620.jpg",
              "price_unit": "/月",
              "type": 6
            },
            {
              "photo": "https://img.ziroom.com/minsu/g2m4/M00/EC/1B/ChAZYWLyLjKANriBAAqrS2LeFk0107.png_Z_930_620.png",
              "subway_station_info": "房源距褡裢坡站步行约3866米",
              "area": "111",
              "tags": [
                {
                  "style": {
                    "background": "#1AFF961E",
                    "color": "#FFFF961E"
                  },
                  "hot": 1,
                  "title": "自如寓"
                }
              ],
              "type": 6,
              "version_name": "10001011",
              "zraExperimentId": "zrasearchstyle",
              "zrrefer": "",
              "location_id": 0,
              "template_type": 1,
              "name": "虾米即将开业房型2·其他",
              "price_unit": "/月",
              "zraGroupId": "doublestyle",
              "price": 77,
              "zra_extra": {
                "zra_display_type": 1,
                "house_type_id": "8a768dc082868ee0018286ae88570066",
                "house_type_name": "虾米即将开业房型2",
                "rent_unit_type": 2,
                "rent_unit": "整租1居",
                "reserve_num": -1,
                "rooms_count": -1,
                "key_points": "整租1居 | 其他",
                "project_id": "8a768d8b8183f13b018183f36ba40004",
                "project_name": "虾米prime"
              }
            }
          ],
          "project_info": {
            "project_tags": [
              {
                "title": "111",
                "background": "#08000000",
                "color": "#99000000"
              },
              {
                "title": "222",
                "background": "#08000000",
                "color": "#99000000"
              },
              {
                "title": "333",
                "background": "#08000000",
                "color": "#99000000"
              }
            ],
            "background": "https://webimg.ziroom.com/d704fb82-28ac-4eaf-9e2d-4d6ada7623e8.png",
            "project_id": "8a768d8b8183f13b018183f36ba40004",
            "project_name": "虾米prime",
            "subway_station_info": "房源距褡裢坡站步行约3866米",
            "router_title": "进入自如寓",
            "target": "ziroomCustomer://zrRentModule/newZraDetailspage",
            "parameter": {
              "projectId": "8a768d8b8183f13b018183f36ba40004"
            }
          }
        },
        "zrrefer": "1602629936451825664|1|4|0|search_result|",
        "location_id": 4,
        "template_type": 2,
        "experimentId": "RankOpt"
      },
      {
        "bizcircle_name": "马家堡",
        "can_sign_date": 1603814400,
        "floor_total": "6",
        "inv_id": "468300",
        "photo": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.jpg",
        "anti_theft_price": [
          "//webimg.ziroom.com/13042b00-831f-4f47-938a-3c819385b6fb.png",
          [
            5,
            3,
            1,
            4
          ]
        ],
        "zrrefer": "1602629936451825664|1|5|0.33760135086307796|search_result|",
        "experimentId": "RankOpt",
        "house_type": 1,
        "name": "西马金润二区3居室-北卧",
        "air_qualified": 1,
        "house_code": "BJZRGY0818209740",
        "lng": 116.386742,
        "price_unit": "/月",
        "resblock_name": "西马金润二区",
        "apartment_type": 1,
        "bedroom": 3,
        "activity_marks": [
          "twoHundredMillion"
        ],
        "face": "北",
        "stock_status": "202",
        "location_id": 5,
        "template_type": 15,
        "photo_min": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.jpg",
        "source": "search",
        "price_style": {
          "color": "#FFFF961E"
        },
        "groupId": "rankOpt4",
        "session_id": "1602629936451825664",
        "ziroom_version_id": 1008,
        "resblock_id": "1111027381060",
        "is_ai_lock": 1,
        "photo_min_webp": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.webp",
        "sale_img": "https://image.ziroom.com/g2m1/M00/85/95/ChAFBlvugreAdUurAAAIJIioF8Q667.png",
        "inv_no": "745425100",
        "lat": 39.845373,
        "floor": "5",
        "photo_webp": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.webp",
        "area": "22.3",
        "area_order": 22.3,
        "id": "61228538",
        "pic_experiment_id": "listUI",
        "price": 3260,
        "sale_status": 4,
        "type": 1,
        "district_name": "丰台",
        "house_id": "60197570",
        "subway_station_info": "房源距角门东站步行约1221米",
        "parlor": 1,
        "pic_group_id": "_cross_left",
        "style_tag": "朝北",
        "city_code": 110000,
        "tags": [
          {
            "style": {
              "color": "#FFFFFFFF",
              "background": "#FF7B93B0"
            },
            "title": "待释放"
          },
          {
            "style": {},
            "title": "新小区"
          }
        ],
        "type_text": "合租",
        "version_name": "1008",
        "can_sign_time": 1561255200,
        "code": "BJZRGY0818209740_01"
      },
      {
        "lat": 40.088074,
        "subway_station_info": "房源距育知路站步行约803米",
        "parlor": 1,
        "price": 2430,
        "resblock_id": "1111027374437",
        "tags": [
          {
            "style": {
              "background": "#FFCCCCCC",
              "color": "#FFFFFFFF"
            },
            "title": "已预订"
          },
          {
            "title": "可短签"
          }
        ],
        "style_tag": "朝南",
        "face": "南",
        "is_ai_lock": 1,
        "pic_group_id": "_cross_left",
        "zrrefer": "1602629936451825664|1|6|0.2687161983128662|search_result|",
        "groupId": "rankOpt4",
        "anti_theft_price": [
          "//webimg.ziroom.com/13042b00-831f-4f47-938a-3c819385b6fb.png",
          [
            3,
            8,
            5,
            4
          ]
        ],
        "source": "search",
        "stock_status": "201",
        "activity_marks": [
          "trainee"
        ],
        "bizcircle_name": "回龙观",
        "code": "BJZRGY0819353069_03",
        "air_qualified": 1,
        "house_id": "60325339",
        "inv_id": "762585",
        "resblock_name": "风雅园二区",
        "bedroom": 3,
        "can_sign_short": 1,
        "photo_webp": "https://img.ziroom.com/pic/static/images/slist_1207/buding-up.jpg_C_240_180_Q100.webp",
        "template_type": 15,
        "apartment_type": 1,
        "id": "62066207",
        "price_style": {
          "color": "#FFFF961E"
        },
        "floor": "4",
        "floor_total": "7",
        "photo_min": "https://img.ziroom.com/pic/static/images/slist_1207/buding-up.jpg_C_240_180_Q100.jpg",
        "air_quality": 2,
        "house_type": 1,
        "pic_experiment_id": "listUI",
        "can_sign_time": 1559080587,
        "type": 1,
        "price_unit": "/月",
        "city_code": 110000,
        "lng": 116.328915,
        "name": "风雅园二区3居室-南卧",
        "location_id": 6,
        "area": "13.5",
        "can_sign_date": 1647964800,
        "district_name": "昌平",
        "photo_min_webp": "https://img.ziroom.com/pic/static/images/slist_1207/buding-up.jpg_C_240_180_Q100.webp",
        "photo": "https://img.ziroom.com/pic/static/images/slist_1207/buding-up.jpg_C_240_180_Q100.jpg",
        "sale_status": 2,
        "ziroom_version_id": 1008,
        "experimentId": "RankOpt",
        "house_code": "BJZRGY0819353069",
        "inv_no": "773970745",
        "type_text": "合租",
        "version_name": "1008",
        "session_id": "1602629936451825664",
        "area_order": 13.5,
        "sale_img": "https://image.ziroom.com/g2m1/M00/85/95/ChAFBlvugreAdUurAAAIJIioF8Q667.png"
      },
      {
        "inv_id": "760400",
        "experimentId": "RankOpt",
        "lng": 116.337,
        "parlor": 1,
        "price": 2860,
        "anti_theft_price": [
          "//webimg.ziroom.com/13042b00-831f-4f47-938a-3c819385b6fb.png",
          [
            3,
            0,
            1,
            4
          ]
        ],
        "bedroom": 4,
        "resblock_name": "北欧印象",
        "floor_total": "28",
        "id": "62059571",
        "name": "北欧印象4居室-南卧",
        "ziroom_version_id": 1008,
        "zrrefer": "1602629936451825664|1|7|0.25515033410254784|search_result|",
        "session_id": "1602629936451825664",
        "area_order": 19.4,
        "pic_experiment_id": "listUI",
        "groupId": "rankOpt4",
        "house_type": 1,
        "photo_min_webp": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.webp",
        "source": "search",
        "style_tag": "朝南",
        "photo_webp": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.webp",
        "apartment_type": 1,
        "photo_min": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.jpg",
        "price_unit": "/月",
        "can_sign_date": 1647964800,
        "inv_no": "773758800",
        "is_ai_lock": 1,
        "version_name": "1008",
        "city_code": 110000,
        "pic_group_id": "_cross_left",
        "sale_status": 2,
        "district_name": "西城",
        "floor": "25",
        "house_code": "BJZRGY0819351961",
        "subway_station_info": "房源距湾子站步行约1712米",
        "price_style": {
          "color": "#FFFF961E"
        },
        "location_id": 7,
        "area": "19.4",
        "code": "BJZRGY0819351961_05",
        "face": "南",
        "lat": 39.8822,
        "air_qualified": 1,
        "house_id": "60324679",
        "tags": [
          {
            "style": {
              "background": "#FFCCCCCC",
              "color": "#FFFFFFFF"
            },
            "title": "已预订"
          },
          {
            "title": "独立阳台",
            "style": {}
          },
          {
            "title": "可短签"
          }
        ],
        "type_text": "合租",
        "air_quality": 2,
        "bizcircle_name": "广安门",
        "type": 1,
        "template_type": 15,
        "can_sign_short": 1,
        "can_sign_time": 1559080518,
        "photo": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.jpg",
        "resblock_id": "1111027376034",
        "stock_status": "201"
      },
      {
        "source": "search",
        "stock_status": "201",
        "apartment_type": 1,
        "bedroom": 5,
        "lat": 40.093038,
        "pic_experiment_id": "listUI",
        "lng": 116.340551,
        "zrrefer": "1602629936451825664|1|8|0.22824040930573142|search_result|",
        "location_id": 8,
        "can_sign_date": 1653580800,
        "groupId": "rankOpt4",
        "id": "61744427",
        "photo": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.jpg",
        "template_type": 15,
        "sale_status": 2,
        "version_name": "1008",
        "air_quality": 2,
        "code": "BJZRGY0818299440_01",
        "is_ai_lock": 1,
        "air_qualified": 1,
        "floor_total": "6",
        "resblock_id": "1111027378165",
        "bizcircle_name": "回龙观",
        "name": "龙禧苑一区5居室-南卧",
        "can_sign_time": 1559079221,
        "house_code": "BJZRGY0818299440",
        "tags": [
          {
            "style": {
              "background": "#FFCCCCCC",
              "color": "#FFFFFFFF"
            },
            "title": "已预订"
          },
          {
            "style": {},
            "title": "独立阳台"
          },
          {
            "title": "可租1年以上"
          }
        ],
        "type": 1,
        "type_text": "合租",
        "anti_theft_price": [
          "//webimg.ziroom.com/13042b00-831f-4f47-938a-3c819385b6fb.png",
          [
            3,
            1,
            6,
            4
          ]
        ],
        "inv_id": "641748",
        "price_unit": "/月",
        "session_id": "1602629936451825664",
        "photo_min_webp": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.webp",
        "style_tag": "朝南",
        "area": "14.6",
        "can_sign_long": 1,
        "photo_webp": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.webp",
        "pic_group_id": "_cross_left",
        "ziroom_version_id": 1008,
        "district_name": "昌平",
        "photo_min": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.jpg",
        "price": 2690,
        "house_id": "60277397",
        "resblock_name": "龙禧苑一区",
        "subway_station_info": "房源距育知路站步行约895米",
        "price_style": {
          "color": "#FFFF961E"
        },
        "parlor": 1,
        "experimentId": "RankOpt",
        "face": "南",
        "floor": "5",
        "inv_no": "762249556",
        "area_order": 14.6,
        "house_type": 1,
        "city_code": 110000
      },
      {
        "area_order": 16.4,
        "floor_total": "16",
        "price": 2390,
        "activity_marks": [
          "trainee"
        ],
        "air_quality": 2,
        "price_style": {
          "color": "#FFFF961E"
        },
        "bedroom": 3,
        "lng": 116.268,
        "city_code": 110000,
        "template_type": 15,
        "groupId": "rankOpt4",
        "id": "62070661",
        "is_ai_lock": 1,
        "parlor": 1,
        "sale_img": "https://image.ziroom.com/g2m1/M00/85/95/ChAFBlvugreAdUurAAAIJIioF8Q667.png",
        "name": "和光里3居室-南卧",
        "zrrefer": "1602629936451825664|1|9|0.21820008575379057|search_result|",
        "face": "南",
        "inv_id": "764130",
        "inv_no": "774120610",
        "photo_min": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.jpg",
        "type": 1,
        "anti_theft_price": [
          "//webimg.ziroom.com/13042b00-831f-4f47-938a-3c819385b6fb.png",
          [
            3,
            5,
            6,
            4
          ]
        ],
        "stock_status": "201",
        "bizcircle_name": "五里店",
        "can_sign_short": 1,
        "code": "BJZRGY0819353771_01",
        "house_id": "60326624",
        "photo": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.jpg",
        "price_unit": "/月",
        "sale_status": 3,
        "tags": [
          {
            "style": {},
            "title": "独立阳台"
          },
          {
            "title": "可短签"
          }
        ],
        "air_qualified": 1,
        "apartment_type": 1,
        "house_type": 1,
        "area": "16.4",
        "district_name": "丰台",
        "pic_group_id": "_cross_left",
        "version_name": "1008",
        "experimentId": "RankOpt",
        "can_sign_time": 1559166546,
        "source": "search",
        "location_id": 9,
        "house_code": "BJZRGY0819353771",
        "lat": 39.8673,
        "photo_webp": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.webp",
        "type_text": "合租",
        "ziroom_version_id": 1008,
        "resblock_id": "1111027374992",
        "photo_min_webp": "https://img.ziroom.com/mona/g2m3/M00/9C/8B/ChAZVF_NkL6AU8wVAAMnw7OiKqI417.jpg_C_240_180_Q100.webp",
        "session_id": "1602629936451825664",
        "subway_station_info": "房源距大井站步行约1613米",
        "can_sign_date": 1649001600,
        "floor": "13",
        "pic_experiment_id": "listUI",
        "resblock_name": "和光里",
        "style_tag": "朝南"
      },
      {
        "inv_id": "753907",
        "pic_group_id": "_cross_left",
        "district_name": "朝阳",
        "price_style": {
          "color": "#FFFF961E"
        },
        "city_code": 110000,
        "location_id": 10,
        "air_qualified": 1,
        "can_sign_time": 1559166396,
        "price": 3360,
        "is_ai_lock": 1,
        "photo_min_webp": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.webp",
        "pic_experiment_id": "listUI",
        "can_sign_short": 1,
        "tags": [
          {
            "style": {
              "background": "#FFCCCCCC",
              "color": "#FFFFFFFF"
            },
            "title": "已预订"
          },
          {
            "style": {},
            "title": "独立阳台"
          },
          {
            "title": "可短签"
          },
          {
            "title": "可租1年以上"
          }
        ],
        "zrrefer": "1602629936451825664|1|10|0.21743331197517968|search_result|",
        "apartment_type": 1,
        "lat": 39.996635,
        "anti_theft_price": [
          "//webimg.ziroom.com/13042b00-831f-4f47-938a-3c819385b6fb.png",
          [
            5,
            5,
            1,
            4
          ]
        ],
        "area_order": 16.1,
        "inv_no": "773128979",
        "style_tag": "朝南",
        "house_id": "60322697",
        "house_type": 1,
        "photo_min": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.jpg",
        "floor": "12",
        "house_code": "BJZRGY0819349404",
        "lng": 116.437122,
        "subway_station_info": "房源距关庄站步行约1169米",
        "photo_webp": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.webp",
        "resblock_name": "育慧里一区",
        "groupId": "rankOpt4",
        "activity_marks": [
          "twoHundredMillion"
        ],
        "area": "16.1",
        "can_sign_date": 1641744000,
        "face": "南",
        "name": "育慧里一区3居室-南卧",
        "sale_img": "https://image.ziroom.com/g2m1/M00/85/95/ChAFBlvugreAdUurAAAIJIioF8Q667.png",
        "session_id": "1602629936451825664",
        "floor_total": "19",
        "id": "62043998",
        "ziroom_version_id": 1008,
        "experimentId": "RankOpt",
        "bedroom": 3,
        "photo": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.jpg",
        "sale_status": 2,
        "bizcircle_name": "亚运村小营",
        "parlor": 1,
        "resblock_id": "1111027381714",
        "stock_status": "201",
        "type_text": "合租",
        "type": 1,
        "version_name": "1008",
        "template_type": 15,
        "air_quality": 2,
        "code": "BJZRGY0819349404_01",
        "price_unit": "/月",
        "source": "search"
      },
      {
        "session_id": "1602629936451825664",
        "floor": "2",
        "photo": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.jpg",
        "sale_status": 2,
        "inv_no": "740219304",
        "lat": 40.0134,
        "can_sign_date": 1661702400,
        "face": "南",
        "pic_experiment_id": "listUI",
        "pic_group_id": "_cross_left",
        "city_code": 110000,
        "groupId": "rankOpt4",
        "bedroom": 3,
        "floor_total": "4",
        "house_code": "BJZRGY0818172754",
        "inv_id": "414632",
        "stock_status": "201",
        "version_name": "1008",
        "anti_theft_price": [
          "//webimg.ziroom.com/13042b00-831f-4f47-938a-3c819385b6fb.png",
          [
            5,
            2,
            6,
            4
          ]
        ],
        "air_qualified": 1,
        "can_sign_time": 1559076106,
        "district_name": "朝阳1",
        "resblock_id": "1111027379519",
        "type": 1,
        "parlor": 1,
        "photo_min": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.jpg",
        "zrrefer": "1602629936451825664|1|11|0.20741553492539877|search_result|",
        "area": "16.6",
        "can_sign_short": 1,
        "code": "BJZRGY0818172754_01",
        "house_id": "60163435",
        "photo_webp": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.webp",
        "price_style": {
          "color": "#FFFF961E"
        },
        "experimentId": "RankOpt",
        "area_order": 16.6,
        "bizcircle_name": "南沙滩",
        "id": "61016295",
        "tags": [
          {
            "style": {
              "background": "#FFCCCCCC",
              "color": "#FFFFFFFF"
            },
            "title": "已预订"
          },
          {
            "style": {},
            "title": "独立阳台"
          },
          {
            "title": "可短签"
          }
        ],
        "is_ai_lock": 1,
        "resblock_name": "双泉堡甲2号院",
        "source": "search",
        "ziroom_version_id": 1008,
        "template_type": 15,
        "apartment_type": 1,
        "house_type": 1,
        "type_text": "合租",
        "lng": 116.376,
        "name": "双泉堡甲2号院3居室-南卧",
        "photo_min_webp": "https://img.ziroom.com/pic/static/images/slist_1207/natie-up.jpg_C_240_180_Q100.webp",
        "style_tag": "朝南",
        "location_id": 11,
        "price_unit": "/月",
        "subway_station_info": "房源距北沙滩站步行约863米",
        "price": 3590
      }
    ],
    "query_session_id": "1602629936451825664",
    "empty_tips": ""
  },
  "code": "200",
  "status": "success",
  "requestId": "90473648:1670931726"
}
  
}
    '''
    '''
        "coupon":{
            "coupon_info":{
                "title":"标题名",
                "subtitle":"副标题"
            }
        },
        "list":[
            {
                "icon":[
                    "json"
                ],
                "imageConfig":{
                    "img":"图片url",
                    "size":12
                },
                "titles":[
                    {
                    "subTitle":"描述",
                    "title":"名称"
                    }
                ]
            }
        ]
    }
}
    '''

    a = {"a": [
        [
            {},
            "",
            ""
        ]
    ]
    }

    json_map = [
        {
            "product": "衣服",
            "type": {
                "type": "白色上衣",
                "activity": [
                    "秒杀活动",
                    "加购送袜子",
                ],

                "company": {
                    "name": "靓仔上衣",
                    "awards": [
                        "最具人气奖",
                        "销量第一"
                    ]
                },

                "details": {
                    "size": "xxl",
                    "color": "白色",
                },

            }
        },

        {
            "product": "鞋子",
            "type": {
                "type": "黑色鞋子",
                "activity": [
                    "运动专属活动"
                ],

                "company": {
                    "name": "耐磨谢业"
                },

                "recommend": {
                    "title": "更多为你推荐",
                    "link": "www.baidu.com"
                }
            }
        }
    ]
    print(json.dumps(json_map,ensure_ascii=False))

    # print(dict(ChainMap(json_map[0],json_map[1])))
    # print({** json_map[0], ** json_map[1]})

    model = [
        {
            'product': '衣服',
            'type': {
                'type': '黑色鞋子',
                'activity': [
                    '秒杀活动',
                    '加购送袜子',
                    '运动专属活动'
                ],
                'recommend': {
                    'title': '更多为你推荐',
                    'link': 'www.baidu.com'
                },
                'company': {
                    'name': '',
                    'awards': [
                        '最具人气奖',
                        '销量第一'
                    ]
                },
                'details': {
                    'size': 'xxl',
                    'color': '白色'
                }
            }
        }
    ]

    json_ = \
        [
            {
                'product': '衣服',
                'type':
                    {'activity':
                        [
                            '秒杀活动',
                            '加购送袜子',
                            '运动专属活动'
                        ],
                        'type': '黑色鞋子',
                        'recommend':
                            {'title': '更多为你推荐', 'link': 'www.baidu.com'}
                    }
            }
        ]
    # print(json.dumps(flattenMap(json_map),ensure_ascii=False))
    # map:dict = json.loads(json_str_array)
    # convertJsonToModel(json_str_array)
    map111 = '''{"modelNameSuffix":"Model","modelNamePrefix":"ZRRent","template_projectNameKey":"json转model","template_userNameKey":"李鹏跃","template_nickNameKey":"lpy","rootModelName":"questionDetails","baseModelName":"ZRBaseModel","modelSavePath":"/Users/lp1/Desktop/pythonProject/iOSTemplateFile","modelData":{"resolveFailInfo":{"router":{"target":"ziroomCustomer://zrRentModule/h5WJFunction","jumpType":"h5","parameter":{"titleBarHidden":"1","url":"https://hot.ziroom.com/2022/zrk-life-pay/?contractCode=BJZYCW82012122012-02"}}},"solutionInfo":{"solutionCode":"aa","solutionName":"aa","problemCode":"aa","components":[{"type":1,"divideType":1,"index":1,"titleInfo":{"icon":"","value":""},"textInfo":{"value":"工作时间%s内首次响应您的诉求  始终跟进问题处理进展%s","needStyles":[{"text":"4小时","style":{"color":"#FFE03810"}},{"text":"直至问题解决","style":{"color":"#FFE03810"}}]},"imageInfos":[{"link":"aa","unit":"px","height":111,"width":666,"index":1}],"buttonInfo":{"title":"生活费用","style":{"textColor":"#FFE03810","borderColor":"#FFE03810","bgColor":"#FFE03810"},"router":{"target":"ziroomCustomer://zrRentModule/h5WJFunction","parameter":{"titleBarHidden":"1","url":"https://hot.ziroom.com/2022/zrk-life-pay/?contractCode=BJZYCW82012122012-02"}}},"orderInfo":{"orderCode":"111","stateInfo":{"stateValue":"1","stateName":"已支付","style":{"color":"#FFE03810"}},"orderTitle":"燃气费(111)","items":[{"questionCn":"表名称","answerCn":"冷水一"}]},"clarificationInfo":{"title":"请选择您遇到的问题","problems":[{"icon":"http://......","title":"对用量有问题","description":"为什么我用了这么多水费","router":{"target":"ziroomCustomer://zrRentModule/h5WJFunction","jumpType":"h5","parameter":{"sceneType":1,"aggregateCode":"","aggregateCollectionCode":"","questionCode":"","originalQuestionCode":"11"}}}]}}]},"createSrInfo":{"hint":"您可以点击下方按钮进行自助立单来反馈您的问题～","title":"去反馈","style":{"textColor":"#FFE03810","borderColor":"#FFE03810","bgColor":"#FFE03810"},"router":{"target":"ziroomCustomer://zrRentModule/h5WJFunction","parameter":{"classficationFourCode":"a","contractCode":"a","cityCode":"10001"}}},"evaluateInfo":{"title":"该答案是否有帮助？","items":[{"title":"","icon":"","nteractiveType":"// 0 直接提交 1 弹窗"},{"title":"","icon":"","interactiveType":"// 0 直接提交 1 弹窗","subInfo":{"uselessTitle":"未帮助到您的原因是？","uselessOptions":[{"value":"1","label":"内容描述不清晰","interactiveType":"//0 直接提交 1 弹窗 文本框"}]}}]},"relatedLores":{"title":"相关问题","items":[{"title":"热门","router":{"target":"ziroomCustomer://zrRentModule/h5WJFunction","parameter":{"classficationFourCode":"a","contractCode":"a","cityCode":"10001"}}}]},"cloudKeeper":{"hint":"联系将台云管家","title":"联系将台云管家","style":{"color":"#FFE03810"},"router":{"target":"","parameter":{}}}}}'''
    # map:dict = json.loads(map111)
    convertJsonToModel(map111)