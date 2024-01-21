
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic
json_config_str_demo = ''''''



# =======================================================================================================

def isBaseTypeWithValue(value):
    return isinstance(value, bool) | isinstance(value, int) | isinstance(value, float) | isinstance(value, str)
def flattenMap(map) -> dict:
    result: dict = {}
    if isinstance(map,list):
        result = mergetList(map)

    if isinstance(map,dict):
        flatten = {}
        for key,value in map.items():
            if (isBaseTypeWithValue(value)) or flatten.get(key) == None:
                flatten[key] = map[key]
                continue
            else:
                merge_map = flattenMap(map)
                flatten = mergeMap(flatten,merge_map)

        result = flatten
    return result

def mergetList(list:list) -> dict:
    map = {}
    for value in list:
        map = mergeMap(map,value)
    return map

def mergeMap(map1:dict,map2:dict) -> dict:
    result = map1.copy()
    for key,value in map2.items():
        map1_value = map1.get(key)
        if map1_value is not None:
            #相同key
            if(isBaseTypeWithValue(value)) == False and isBaseTypeWithValue(map1_value):
                result[key] = flattenMap(value)
            elif (isBaseTypeWithValue(value)) and isBaseTypeWithValue(map1_value):
                continue
            else:
                result[key] = mergeMap(value,map1_value)
        else:
            result[key] = value
    result = flattenMap(result)
    return result
