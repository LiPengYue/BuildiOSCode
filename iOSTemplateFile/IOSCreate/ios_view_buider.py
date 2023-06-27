import json
from iOSTemplateFile.IOSCreate.ios_base_view import ios_base_view as IView
from iOSTemplateFile.IOSCreate.ios_label import ios_label as ILabel
from iOSTemplateFile.IOSCreate.ios_button import ios_button as IButton
from iOSTemplateFile.IOSCreate.ios_image_view import ios_image_view as IImageView
from iOSTemplateFile.IOSCreate.ios_constraints_maker import ios_constraints_maker as IConstraintsMaker
from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_view_model import ios_view_model as IViewModel
from iOSTemplateFile.IOSCreate import ios_class_create as ICreate
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic
from iOSTemplateFile.IOSCreate.ios_view_factory import ios_view_factory as IViewFactory
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

iOSTemplateViewPathKey = 'templateViewPath'
iOSTemplateViewModelPathKey = 'templateViewModelPath'

iOSTemplateViewNameKey = 'templateViewName'
iOSTemplateBaseViewNameKey = 'templateBaseViewName'
iOSTemplateViewModelNameKey = 'templateViewModelName'
iOSTemplateBaseViewModelNameKey = 'templateBaseViewModelName'

# View 创建
class ios_view_buider:

    def createView(self,ViewJson):
        ViewJsonMap = {}
        if isinstance(ViewJson,str) == True:
            ViewJsonMap = json.loads(ViewJson)
        if isinstance(ViewJson,dict) == True:
            ViewJsonMap = ViewJson

        ViewName = ViewJsonMap.get(IStatic.IOS_TEMPLATE_JSON_ViewNameKey,ViewJsonMap[IStatic.IOS_TEMPLATE_JSON_PropertyTypeKey])
        if IStatic.str_is_empty(ViewName):
            ViewName = 'XIBParserView'
        viewModelName = ViewJsonMap.get(IStatic.IOS_TEMPLATE_JSON_ViewModelKey,'')
        if IStatic.str_is_empty(viewModelName):
            viewModelName = ICreate.getClassNameStr('',f"{ViewName}ViewModel",'')
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

        # SubViews = ViewJsonMap[IStatic.IOS_TEMPLATE_JSON_SubViewsKey]

        ViewPropertyAppend = '\n'
        ViewApiSetterAppend = '\n'
        ViewGetterAndSetterAppend = ''
        ViewConstraintsAppend = '\n'
        ViewAddSubViewAppend = ''
        ViewMImportAppend = ''
        rootViewFactory:IViewFactory = IViewFactory(self_holder_pointer_name='self',
                                                    datasource=dataSourceName,
                                                    datasource_holder_pointer_name='self',
                                                    viewDic=ViewJsonMap)

        ViewPropertyAppend += '\n'.join(rootViewFactory.viewPropertyAppendList)
        ViewApiSetterAppend += '\n'.join(rootViewFactory.viewApiSetterAppendList)
        ViewGetterAndSetterAppend += '\n'.join(rootViewFactory.viewGetterAndSetterAppendList)
        ViewConstraintsAppend += '\n'.join(rootViewFactory.viewConstaintsAppendList)
        ViewAddSubViewAppend += '\n'.join(rootViewFactory.viewAddSubViewAppendList)
        ViewMImportAppend += rootViewFactory.viewMImportAppendStr
        view_model.add_property_list(rootViewFactory.viewModelPropertyNameList)

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
    # ViewM_property_re = re.search(Regular_StartCellMAPIKey, str, flags=re.DOTALL)
    # print(ViewM_property_re)
    # View_property_location = ViewM_property_re.end()
    # ViewJson = input('请输入ViewJson')
    view_json:str = JsonConfigStr.json_config_str()
