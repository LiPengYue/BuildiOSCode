
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic
json_config_str_demo = '''
 {
    
	"template_projectNameKey": "生成View",
	"template_userNameKey": "李鹏跃",
	"template_nickNameKey": "lpy",
	
	"ViewName": "ZRFastReserveDetailHoseCardCell",
    "ViewModelName": "ZRFastReserveDetailHoseCardViewModel",
    "BaseViewModelName": "ZRFastReserveDetailBaseViewModel",
    "DataSouceName":"viewModel",
    
    "TemplateViewName": "iOSTemplateTableViewCell",
    "TemplateBaseViewName": "ZRRentBaseTableViewCell",
    "TemplateViewModelName": "iOSTemplateViewModel",
    "TemplateTableBaseViewModelName": "iOSTemplateTableBaseViewModel",
    "TemplateViewPath": "/Users/lp1/Desktop/pythonProject/iOSTemplateFile/iOSTemplate",
    "TemplateViewModelPath":"/Users/lp1/Desktop/pythonProject/iOSTemplateFile/iOSTemplate",
    
	"SavePath": "/Users/lp1/01我的文件/一些资料/code/2.Client_fork/1. demos/AVPlayer/AVPlayer/Demos/PythonMakeCode",
	
	"SubViews": [{
			"PropertyType": "UILabel",
			"PropertyName": "titleLabel",
			"APINameKey": "title",
			
			"BorderColor" : "0xFF00FF00",
            "TextColor" : "#FF00FF00",
            "BackgroundColor" : "bgColor",
            "BorderWidth" : "12",
            "CornerRadius" : "3",
            "MasksToBounds" : "true",
			
			"Constraints": {
				"Height": "100",
				"Width": "300",
				"Top": {
					"View": "",
					"Space": "100",
					"Location": ""
				},
				"Left": {
					"View": "",
					"Space": "120",
					"Location": ""
				}
			}
		},
		{
			"PropertyType": "UILabel",
			"PropertyName": "subtitleLabel",
			"APINameKey": "subtitle",

            
			"Constraints": {
				"Top": {
					"View": "titleLabel",
					"Space": "10",
					"Location": "bottom"
				},
				"Left": {
					"View": "",
					"Space": "120",
					"Location": ""
				},
				"Bottom": {
					"Space": "-100",
					"Location": ""
				},
				"Right": {
					"View": "titleLabel",
					"Space": "0",
					"Location": ""
				}
			}
		}
		,
		{
			"PropertyType": "ZRSVGATabbarButtonView",
			"PropertyName": "customeLabel",
			"APINameKey": "subtitle",

            
			"Constraints": {
				"Top": {
					"View": "titleLabel",
					"Space": "10",
					"Location": "bottom"
				},
				"Left": {
					"View": "",
					"Space": "120",
					"Location": ""
				},
				"Bottom": {
					"Space": "-100",
					"Location": ""
				},
				"Right": {
					"View": "titleLabel",
					"Space": "0",
					"Location": ""
				}
			}
		},
		{
			"PropertyType": "ZRSVGATabbarButtonView",
			"PropertyName": "baseCustomeLabel",
			"APINameKey": "subtitle",

            
			"Constraints": {
				"Top": {
					"View": "titleLabel",
					"Space": "10",
					"Location": "bottom"
				},
				"Left": {
					"View": "",
					"Space": "120",
					"Location": ""
				},
				"Bottom": {
					"Space": "-100",
					"Location": ""
				},
				"Right": {
					"View": "titleLabel",
					"Space": "0",
					"Location": ""
				}
			}
		},
		{
			"PropertyType": "UIImageView",
			"PropertyName": "bgImageView",
			"APINameKey": "bgImage",
			
			"BorderColor" : "0xFF00FF00",
            "TextColor" : "#FF00FF00",
            "BackgroundColor" : "bgColor",
            "BorderWidth" : "12",
            "CornerRadius" : "3",
            "MasksToBounds" : "true",
            "ImageName":"ImageName"
			
		},
		{
			"PropertyType": "UIButton",
			"PropertyName": "bgButton",
			"APINameKey": "buttonText",
			
			"BorderColor" : "0xFF00FF00",
            "TextColor" : "#FF00FF00",
            "BackgroundColor" : "bgColor",
            "BorderWidth" : "12",
            "CornerRadius" : "3",
            "MasksToBounds" : "true"
		}
	]
}
    '''



# =======================================================================================================
'''
 "BackgroundColor" : "bgColor",
            "BorderWidth" : "12",
            "CornerRadius" : "3",
            "MasksToBounds" : "true",
'''
def json_config_str():
    return '''
 {
    "template_projectNameKey":"生成View",
    "template_userNameKey":"李鹏跃",
    "template_nickNameKey":"lpy",
    "ViewName":"ZRFastReserveDetailHoseCardCell",
    "ViewModelName":"ZRFastReserveDetailHoseCardViewModel",
    "BaseViewModelName":"ZRFastReserveDetailBaseViewModel",
    "DataSouceName":"viewModel",
    "TemplateViewName":"iOSTemplateTableViewCell",
    "TemplateBaseViewName":"ZRRentBaseTableViewCell",
    "TemplateViewModelName":"iOSTemplateViewModel",
    "TemplateTableBaseViewModelName":"iOSTemplateTableBaseViewModel",
    "TemplateViewPath":"/Users/lp1/Desktop/pythonProject/iOSTemplateFile/iOSTemplate",
    "TemplateViewModelPath":"/Users/lp1/Desktop/pythonProject/iOSTemplateFile/iOSTemplate",
    "SavePath":"/Users/lp1/01我的文件/一些资料/code/2.Client_fork/1. demos/AVPlayer/AVPlayer/Demos/PythonMakeCode",
    "SubViews":[
        {
            "PropertyType":"UIImageView",
            "PropertyName":"houseCoverImageView",
            "APINameKey":"cover",
            "CornerRadius":2,
            "MasksToBounds":"true",
            "Constraints":{
                "Height":"90",
                "Width":"120",
                "Top":{
                    "View":"",
                    "Space":"16",
                    "Location":""
                },
                "Left":{
                    "View":"",
                    "Space":"16",
                    "Location":""
                }
            }
        },
        {
            "PropertyType":"UILabel",
            "PropertyName":"houseNameLabel",
            "APINameKey":"title",
            "TextColor":"KColor_C1_85",
            "FontFamily":"PingFangSC-Regular",
            "FontSize":"15",
            "Constraints":{
                "Height":"18",
                "Top":{
                    "View":"houseCoverImageView",
                    "Space":"0"
                },
                "Left":{
                    "View":"houseCoverImageView",
                    "Space":"12",
                    "Location":"Right"
                },
                "Right":{
                    "View":"",
                    "Space":"-16"
                }
            }
        },
        {
            "PropertyType":"UILabel",
            "PropertyName":"priceLabel",
            "APINameKey":"price",
            "FontFamily":"PingFangSC-Regular",
            "FontSize":"15",
            "Constraints":{
                "Height":"18",
                "Top":{
                    "View":"houseNameLabel",
                    "Space":"8"
                },
                "Left":{
                    "View":"houseNameLabel"
                },
                "Right":{
                    "View":"houseNameLabel"
                }
            }
        },
        {
            "PropertyType":"UIView",
            "PropertyName":"tipBgView",
            "CornerRadius":0,
            "MasksToBounds":"true",
            "BackgroundColor":"#1AE03810",
            "Constraints":{
                "Top":{
                    "View":"priceLabel",
                    "Space":"8",
                    "Location":"bottom"
                },
                "Left":{
                    "View":"houseCoverImageView",
                    "Space":"10",
                    "Location":"Right"
                },
                "Right":{
                    "View":"houseNameLabel11"
                }
            }
        },
        {
            "PropertyType":"UILabel",
            "PropertyName":"tipLabel",
            "APINameKey":"tip",
            "FontFamily":"PingFangSC-Regular",
            "FontSize":"10",
            "Constraints":{
                "Height":"18",
                "Top":{
                    "View":"tipBgView",
                    "Space":"8"
                },
                "Left":{
                    "View":"tipBgView",
                    "Space":"6"
                },
                "Right":{
                    "View":"tipBgView",
                    "Space":"-6"
                },
                "Bottom":{
                    "View":"tipBgView"
                }
            }
        },
        {
            "PropertyType":"UIView",
            "PropertyName":"hotBgView",
            "CornerRadius":4,
            "MasksToBounds":"true",
            "BackgroundColor":"#08000000",
            "Constraints":{
                "Top":{
                    "View":"houseCoverImageView",
                    "Space":"10",
                    "Location":"bottom"
                },
                "Left":{
                    "View":"houseCoverImageView",
                    "Space":"0",
                    "Location":""
                },
                "Bottom":{
                    "View":"",
                    "Space":"-16",
                    "Location":""
                },
                "Right":{
                    "View":"",
                    "Space":"-16",
                    "Location":""
                }
            }
        },
        {
            "PropertyType":"UILabel",
            "PropertyName":"hotTipLabel",
            "APINameKey":"hotTipStr",
            "TextColor":"hotTipTextColor",
            "FontFamily":"PingFangSC-Regular",
            "FontSize":"12",
            "Constraints":{
                "Top":{
                    "View":"hotBgView",
                    "Space":"0"
                },
                "Bottom":{

                },
                "Left":{
                    "View":"hotBgView",
                    "Space":"10"
                }
            }
        },
        {
            "PropertyType":"UILabel",
            "PropertyName":"hotTipInfoLabel",
            "APINameKey":"hotTipInfoStr",
            "TextColor":"hotTipInfoTextColor",
            "FontFamily":"PingFangSC-Regular",
            "FontSize":"12",
            "Constraints":{
                "Top":{
                    "View":"hotBgView",
                    "Space":"0"
                },
                "Bottom":{

                },
                "Left":{
                    "View":"hotTipLabel",
                    "Space":"8"
                },
                "Right":{
                    "View":"hotBgView",
                    "Space":"-10"
                }
            }
        }
    ]
}
    '''

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
