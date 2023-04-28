import json
from iOSTemplateFile.IOSCreate.ios_base_view import ios_base_view as IView
from iOSTemplateFile.IOSCreate.ios_label import ios_label as ILabel
from iOSTemplateFile.IOSCreate.ios_button import ios_button as IButton
from iOSTemplateFile.IOSCreate.ios_image_view import ios_image_view as IImageView
from iOSTemplateFile.IOSCreate.ios_constraints_maker import ios_constraints_maker as IConstraintsMaker
from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_view_model import ios_view_model as IViewModel
from iOSTemplateFile.IOSCreate import ios_class_create as ICreate
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic
import json_config_str as JsonConfigStr

import iOSTemplateFile.IOSTemplateRegulars as IRegulars
import re

'''
propertyKeys
'''
PropertyStringKey = "@property (nonatomic,copy) NSString *"
PropertyArrayKey = "@property (nonatomic,copy) NSArray *"
PropertyDicKey = "@property (nonatomic,copy) NSDictionary *"
PropertyUILabelKey = "@property (nonatomic,strong) UILabel *"
PropertyUIButtonKey = "@property (nonatomic,strong) UIButton *"
PropertyUIImageViewKey = "@property (nonatomic,strong) UIImageView *"

iOSTemplateViewPathKey = 'TemplateViewPath'
iOSTemplateViewModelPathKey = 'TemplateViewModelPath'

iOSTemplateViewNameKey = 'TemplateViewName'
iOSTemplateBaseViewNameKey = 'TemplateBaseViewName'
iOSTemplateViewModelNameKey = 'TemplateViewModelName'
iOSTemplateBaseViewModelNameKey = 'TemplateTableBaseViewModelName'

# View 创建
class ios_code_build:

    def createView(self,ViewJson):
        ViewJsonMap = json.loads(ViewJson)
        ViewName = ViewJsonMap[IStatic.IOS_TEMPLATE_JSON_ViewNameKey]
        viewModelName = ViewJsonMap[IStatic.IOS_TEMPLATE_JSON_ViewModelKey]
        BaseViewModelName = ViewJsonMap[IStatic.IOS_TEMPLATE_JSON_BaseViewModelKey]
        savePath = ViewJsonMap[IStatic.IOS_TEMPLATE_JSON_SavePathKey]
        dataSourceName = ViewJsonMap.get(IStatic.IOS_TEMPLATE_JSON_DataSouceName,'viewModel')

        template_ViewName = ViewJsonMap[iOSTemplateViewNameKey]
        template_ViewH_FileName = ViewJsonMap[iOSTemplateViewPathKey] + '/' + template_ViewName + '.h'
        template_ViewM_FileName = ViewJsonMap[iOSTemplateViewPathKey]  + '/' + template_ViewName + '.m'

        template_BaseViewModelName = ViewJsonMap[iOSTemplateBaseViewModelNameKey]
        template_ViewModelName = ViewJsonMap[iOSTemplateViewModelNameKey]
        template_viewModelH_FileName = ViewJsonMap[iOSTemplateViewModelPathKey] + '/' + template_ViewModelName + '.h'
        template_viewModelM_FileName = ViewJsonMap[iOSTemplateViewModelPathKey] + '/' + template_ViewModelName + '.m'
        view_model = IViewModel(baseViewModelName=BaseViewModelName,
                                viewModelName=viewModelName,
                                template_baseViewModelName=template_BaseViewModelName,
                                template_viewModelName=template_ViewModelName,
                                template_viewModelH_FileName=template_viewModelH_FileName,
                                template_viewModelM_FileName=template_viewModelM_FileName)

        # 打开文件
        with open(template_ViewH_FileName, "r") as f:
            template_ViewH = f.read()
        with open(template_ViewM_FileName, "r") as f:
            template_ViewM = f.read()
        with open(template_viewModelH_FileName, "r") as f:
            template_viewModelH = f.read()
        with open(template_viewModelM_FileName, "r") as f:
            template_viewModelM = f.read()

        SubViews = ViewJsonMap[IStatic.IOS_TEMPLATE_JSON_SubViewsKey]

        ViewPropertyAppend = '\n'
        ViewApiSetterAppend = '\n'
        ViewGetterAndSetterAppend = ''
        ViewConstraintsAppend = ''
        ViewAddSubViewAppend = ''
        ViewMImportAppend = ''

        for propertyMap in SubViews:
            # ViewM property
            propertyType = propertyMap[IStatic.IOS_TEMPLATE_JSON_PropertyTypeKey]
            propertyName = propertyMap[IStatic.IOS_TEMPLATE_JSON_PropertyNameKey]
            backgroundColor = propertyMap.get(IStatic.IOS_TEMPLATE_JSON_BackgroundColorKey, '')
            borderColor = propertyMap.get(IStatic.IOS_TEMPLATE_JSON_BorderColorKey, '')
            borderWidth = propertyMap.get(IStatic.IOS_TEMPLATE_JSON_BorderWidthKey, '')
            cornerRadius = propertyMap.get(IStatic.IOS_TEMPLATE_JSON_CornerRadiusKey, '')
            masksToBounds = propertyMap.get(IStatic.IOS_TEMPLATE_JSON_MasksToBoundsKey, '')


            text_alignment = propertyMap.get(IStatic.IOS_TEMPLATE_JSON_MasksTo_TextAlignment, IStatic.IOS_TEMPLATE_NSTextAlignmentLeft)
            font_family = propertyMap.get(IStatic.IOS_TEMPLATE_JSON_MasksTo_FontFamily, '')
            font_size = propertyMap.get(IStatic.IOS_TEMPLATE_JSON_MasksTo_FontSize, '')
            text_color = propertyMap.get(IStatic.IOS_TEMPLATE_JSON_MasksTo_TextColor, '')

            imageName = propertyMap.get(IStatic.IOS_TEMPLATE_JSON_MasksTo_ImageName, '')
            apiName = propertyMap.get(IStatic.IOS_TEMPLATE_JSON_APINameKey,'')

            view_model.add_property(apiName)
            view_model.add_color_property_ifNeeded(backgroundColor)
            view_model.add_color_property_ifNeeded(borderColor)

            ViewConstraintsAppend += IConstraintsMaker(propertyMap).makeForMap()

            if propertyType == IStatic.IOS_TEMPLATE_JSON_UILabelKey:
                label = ILabel(self_holder_pointer_name='self',
                               type=propertyType,
                               name=propertyName,
                               datasource=dataSourceName,
                               datasource_holder_pointer_name='self',
                               background_color=backgroundColor,
                               border_color=borderColor,
                               border_width=borderWidth,
                               corner_radius=cornerRadius,
                               masks_to_bounds=masksToBounds,
                               title=apiName,
                               font_family=font_family,
                               font_size=font_size,
                               text_color=text_color,
                               text_alignment_name=text_alignment)
                ViewPropertyAppend += label.property()
                ViewApiSetterAppend += label.propertys_set_data_str()
                ViewAddSubViewAppend += label.move_to_super_view('')
                ViewGetterAndSetterAppend += label.lazy_load()

            elif propertyType == IStatic.IOS_TEMPLATE_JSON_UIButtonKey:
                button = IButton(self_holder_pointer_name='self',
                                 type=propertyType,
                                 name=propertyName,
                                 datasource=dataSourceName,
                                 datasource_holder_pointer_name='self',
                                 background_color=backgroundColor,
                                 border_color=borderColor,
                                 border_width=borderWidth,
                                 corner_radius=cornerRadius,
                                 masks_to_bounds=masksToBounds,
                                 title=apiName,
                                 font_family=font_family,
                                 font_size=font_size,
                                 text_color=text_color,
                                 text_alignment_name=text_alignment)
                ViewPropertyAppend += button.property()
                ViewApiSetterAppend += button.propertys_set_data_str()
                ViewAddSubViewAppend += button.move_to_super_view('')
                ViewGetterAndSetterAppend += button.lazy_load()

            elif propertyType == IStatic.IOS_TEMPLATE_JSON_UIImageViewKey:
                imageView = IImageView(self_holder_pointer_name='self',
                                       type=propertyType,
                                       name=propertyName,
                                       datasource=dataSourceName,
                                       datasource_holder_pointer_name='self',
                                       background_color=backgroundColor,
                                       border_color=borderColor,
                                       border_width=borderWidth,
                                       corner_radius=cornerRadius,
                                       masks_to_bounds=masksToBounds,
                                       image_url=apiName,
                                       image_name=imageName)
                ViewPropertyAppend += imageView.property()
                ViewApiSetterAppend += imageView.propertys_set_data_str()
                ViewAddSubViewAppend += imageView.move_to_super_view('')
                ViewGetterAndSetterAppend += imageView.lazy_load()
            else:
                view = IView(self_holder_pointer_name='self',
                             type=propertyType,
                             name=propertyName,
                             datasource=dataSourceName,
                             datasource_holder_pointer_name='self',
                             background_color=backgroundColor,
                             border_color=borderColor,
                             border_width=borderWidth,
                             corner_radius=cornerRadius,
                             masks_to_bounds=masksToBounds)
                ViewMImportAppend = view.import_class_str(did_imporrt_str=ViewMImportAppend)
                print(ViewMImportAppend)
                ViewPropertyAppend += view.property()
                ViewApiSetterAppend += view.propertys_set_data_str()
                ViewAddSubViewAppend += view.move_to_super_view('')
                ViewGetterAndSetterAppend += view.lazy_load()

            ViewApiSetterAppend += '\n'
            ViewPropertyAppend += '\n'
            ViewAddSubViewAppend += '\n'

        #ViewM property
        template_ViewM = ViewMImportAppend + template_ViewM
        template_ViewM = IRegulars.insert_str(IRegulars.Regular_StartPropertyKey(), ViewPropertyAppend,template_ViewM)

        #ViewM api
        template_ViewM = IRegulars.insert_str(IRegulars.Regular_StartSetUpPropertyKey(), ViewApiSetterAppend,template_ViewM)

        #ViewM getter and setter
        template_ViewM = IRegulars.insert_str(IRegulars.Regular_GeeterAndSetterKey(),ViewGetterAndSetterAppend,template_ViewM)

        # ViewM constraints
        template_ViewM = IRegulars.insert_str(IRegulars.Regular_ConstraintsKey(),'\n' + ViewAddSubViewAppend + ViewConstraintsAppend,template_ViewM)

        #viewModelH property
        template_viewModelH = IRegulars.insert_str(IRegulars.Regular_StartPropertyKey(), view_model.get_properts(), template_viewModelH)

        # viewModelM
        # viewmodelM_re = re.search(Regular_StartCellMAPIKey )
        template_ViewH = IRegulars.remove_regular_str(IRegulars.Regular_StartPropertyKey(), template_ViewH)
        # ViewM property
        template_ViewM = IRegulars.remove_regular_str(IRegulars.Regular_StartPropertyKey(), template_ViewM)
        # ViewM api
        template_ViewM = IRegulars.remove_regular_str(IRegulars.Regular_StartSetUpPropertyKey(),template_ViewM)
        # ViewM getter and setter
        template_ViewM = IRegulars.remove_regular_str(IRegulars.Regular_GeeterAndSetterKey(),template_ViewM)
        # ViewM constraints
        template_ViewM = IRegulars.remove_regular_str(IRegulars.Regular_ConstraintsKey(), template_ViewM)
        # viewModelH property
        template_viewModelH = IRegulars.remove_regular_str(IRegulars.Regular_StartPropertyKey(),template_viewModelH)


        #替换类名
        template_ViewH = re.sub(template_ViewName,ViewName, template_ViewH, count=0,flags=0)
        template_ViewH = re.sub(template_ViewModelName, viewModelName, template_ViewH,count=0,flags=0)
        template_ViewM = re.sub(template_ViewModelName, viewModelName,template_ViewM,count=0,flags=0)
        template_ViewM =  re.sub(template_ViewName,ViewName, template_ViewM,count=0,flags=0)

        template_viewModelH = re.sub(template_ViewName,ViewName,template_viewModelH, count=0,flags=0)
        template_viewModelH = re.sub(template_ViewModelName,viewModelName,template_viewModelH,count=0,flags=0)
        template_viewModelH = re.sub(template_BaseViewModelName, BaseViewModelName, template_viewModelH, count=0, flags=0)
        template_viewModelM = re.sub(template_ViewModelName, viewModelName,template_viewModelM,count=0,flags=0)
        template_viewModelM = re.sub(template_ViewName,ViewName,template_viewModelM,count=0,flags=0)


        # save
        ViewPath = savePath
        View_content_desc = ICreate.getFileDescForMap(ViewJsonMap,ViewName)
        ICreate.saveFile(template_ViewM, ViewPath + '/Cells', ViewName + ".m",View_content_desc)
        ICreate.saveFile(template_ViewH, ViewPath + '/Cells', ViewName + ".h",View_content_desc)

        viewModel_content_desc = ICreate.getFileDescForMap(ViewJsonMap, viewModelName)
        ICreate.saveFile(template_viewModelH, ViewPath + '/ViewModels', viewModelName + ".h",viewModel_content_desc)
        ICreate.saveFile(template_viewModelM, ViewPath + '/ViewModels', viewModelName + ".m",viewModel_content_desc)


if __name__ == '__main__':
    '''
    主函数：程序入口
    '''
    str = '''
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
    str = '''
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

    # ViewM_property_re = re.search(Regular_StartCellMAPIKey, str, flags=re.DOTALL)
    # print(ViewM_property_re)
    # View_property_location = ViewM_property_re.end()
    # ViewJson = input('请输入ViewJson')
    view_json:str = JsonConfigStr.json_config_str()
    # with open(template_ViewH_FileName, "r") as f:

    ios_code_build().createView(view_json)

'''
json事例
{"template_projectNameKey":"生成View","template_userNameKey":"李鹏跃","template_nickNameKey":"lpy","CellName":"ZRKeeperCustomerServiceCenterSearchCell","ViewModelName":"ZRKeeperCustomerServiceCenterSearchViewModel","SavePathKey":"/Users/lp1/01我的文件/一些资料/code/2.Client_fork/1. demos/AVPlayer/AVPlayer/Demos/PythonMakeCode","BaseViewModelName":"ZRKeeperCustomerServiceCenterBaseViewModel","SavePath":"/Users/lp1/01我的文件/一些资料/code/demo","CellContent":[{"PropertyType":"UILabel","PropertyName":"titleLabel","APINameKey":"title","Constraints":{"Height":"100","Width":"300","Top":{"View":"","Space":"100","Location":""},"Left":{"View":"","Space":"120","Location":""}}},{"PropertyType":"UILabel","PropertyName":"subtitleLabel","APINameKey":"subtitle","Constraints":{"Top":{"View":"titleLabel","Space":"10","Location":"bottom"},"Left":{"View":"","Space":"120","Location":""},"Bottom":{"Space":"-100","Location":""},"Right":{"View":"titleLabel","Space":"0","Location":""}}},{"PropertyType":"UIImageView","PropertyName":"bgImageView","APINameKey":"bgImage"},{"PropertyType":"UIButton","PropertyName":"bgButton","APINameKey":"buttonText"}]}
'''