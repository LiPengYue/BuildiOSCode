from iOSTemplateFile.IOSCreate.ios_base_view import ios_base_view as IBaseView
from iOSTemplateFile.IOSCreate.ios_label import ios_label as ILabel
from iOSTemplateFile.IOSCreate.ios_button import ios_button as IButton
from iOSTemplateFile.IOSCreate.ios_image_view import ios_image_view as IImageView
from iOSTemplateFile.IOSCreate.ios_constraints_maker import ios_constraints_maker as IConstraintsMaker
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic
import weakref

class ios_view_factory():

    viewDic:dict = {}
    self_holder_pointer_name: str = ''
    datasource: str = ''
    datasource_holder_pointer_name: str = ''

    view: IBaseView = None
    parentView:weakref = None
    subViews: {str:IBaseView} = {}
    subFactoryDic:{str:any} = {}
    superFactory:weakref = None

    # 约束生成器
    constraintsMaker: IConstraintsMaker = None

    #view.m 文件 import 文件
    viewMImportAppendStr:str = ''
    #view.m 文件 property
    viewPropertyAppendList: list = [str]
    #view.m 文件 property 更新网络数据
    viewApiSetterAppendList: list = [str]
    #view.m 文件 addSubviews:
    viewAddSubViewAppendList: list = [str]
    # view.m 文件 constraints
    viewConstaintsAppendList: list = [str]
    #view.m 文件 getter && setter
    viewGetterAndSetterAppendList: list = [str]
    #viewModel.h property
    viewModelPropertyNameList: list = [str]
    viewModelPropertyNameList: list = [str]


    def __init__(self,
                 self_holder_pointer_name:str = '',
                 datasource:str = '',
                 datasource_holder_pointer_name:str = '',
                 viewDic:dict = None,
                 superFactory:any = None,
                 parentView: IBaseView = None
                 ):
        self.viewDic = viewDic
        if superFactory is not None:
            self.superFactory = weakref.ref(superFactory)
        if parentView is not None:
            self.parentView = weakref.ref(parentView)
        self.self_holder_pointer_name = self_holder_pointer_name
        self.datasource = datasource
        self.datasource_holder_pointer_name = datasource_holder_pointer_name
        self.createView()
        self.createConstraintsMaker()
        self.reloadAppendStrs()


    def createView(self):

        propertyType = self.viewDic[IStatic.IOS_TEMPLATE_JSON_PropertyTypeKey]
        view:IBaseView
        if propertyType == IStatic.IOS_TEMPLATE_JSON_UILabelKey:
            view = ILabel(self_holder_pointer_name=self.self_holder_pointer_name,
                          datasource=self.datasource,
                          datasource_holder_pointer_name=self.datasource_holder_pointer_name,
                          jsonDic=self.viewDic
                          )

        elif propertyType == IStatic.IOS_TEMPLATE_JSON_UIButtonKey:
            view = IButton(self_holder_pointer_name=self.self_holder_pointer_name,
                           datasource=self.datasource,
                           datasource_holder_pointer_name=self.datasource_holder_pointer_name,
                           jsonDic=self.viewDic
                           )

        elif propertyType == IStatic.IOS_TEMPLATE_JSON_UIImageViewKey:
            view = IImageView(self_holder_pointer_name=self.self_holder_pointer_name,
                              datasource=self.datasource,
                              datasource_holder_pointer_name=self.datasource_holder_pointer_name,
                              jsonDic=self.viewDic
                              )
        else:
            view = IBaseView(self.self_holder_pointer_name,
                             datasource=self.datasource,
                             datasource_holder_pointer_name=self.datasource_holder_pointer_name,
                             jsonDic=self.viewDic)
        self.view = view
        if self.parentView is not None:
            self.view.parentView = self.parentView
        self.createSubviewFactory()

    def createSubviewFactory(self):
        subViewsDic = self.view.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_SubViewsKey,{})
        subFactoryDic = {}
        subViews = {}
        for key, value in subViewsDic.items():
            subFactory = ios_view_factory(
                self_holder_pointer_name=self.self_holder_pointer_name,
                datasource=self.datasource,
                datasource_holder_pointer_name=self.datasource_holder_pointer_name,
                parentView=self.view,
                viewDic=value,
                superFactory=self
            )
            subFactoryDic[key] = subFactory
            subViews[key] = subFactory.view

        self.subFactoryDic = subFactoryDic
        self.subViews = subViews

    def createConstraintsMaker(self):
        self.constraintsMaker = IConstraintsMaker(self.viewDic)
        @self.constraintsMaker.getViewOwnerNameCallback
        def getViewOwnerNameCallback(viewId:str) -> str:
            # viewDic = self.getViewDicWithViewId(viewId)
            # if viewDic is None:
                # print(viewId)
            if self.getRootFactory().view.id == viewId:
                return 'self'
            viewDic = self.getViewDicWithViewId(viewId)
            if viewDic is None:
                viewDic = self.getViewDicWithViewId(self.superFactory().view.id)
            if viewDic is None:
                return 'self'
            name = viewDic.get(IStatic.IOS_TEMPLATE_JSON_PropertyNameKey,None)
            if IStatic.str_is_empty(name):
                return 'self'
            return f'self.{name}'

            # if viewId == self.view.id:
            #     if self.superFactory is None:
            #         return 'self'
            #     return f'self.{self.view.propertyName}'
            # subview = self.subViews.get(viewId, None)
            # if subview is not None:
            #     return f'self.{subview.propertyName}'
            #
            # if self.superFactory().view.id == viewId:
            #     if self.superFactory().superFactory is None:
            #         return 'self'
            #     return self.superFactory().view.propertyName

        self.constraintsMaker.reload_propertys()

    def getFactoryViewWithId(self,viewId:str):
        rootFactory = self.getRootFactory()
        return rootFactory.getSubFactoryWithId(viewId)

    def getRootFactory(self):
        rootFactory = self
        while rootFactory.superFactory is not None:
            rootFactory = rootFactory.superFactory()
        return rootFactory

    def getViewDicWithViewId(self,viewId:str) -> dict:
        rootFactory:ios_view_factory = self.getRootFactory()
        viewDic:dict = rootFactory.viewDic.get(viewId,None)
        if isinstance(viewDic,dict):
            return viewDic
        viewDic = rootFactory.viewDic
        return self.getSubviewDicWithViewId(viewDic,viewId)

    def getSubviewDicWithViewId(self,subviewDic:dict,viewId:str):
        if subviewDic is None or isinstance(subviewDic,dict) is False or len(subviewDic) == 0:
            return None
        viewDic = subviewDic.get(viewId,None)
        if viewDic is not None and isinstance(viewDic,dict):
            return viewDic

        for key, nexSubviewDic in subviewDic.items():
            viewDic = self.getSubviewDicWithViewId(nexSubviewDic,viewId)
            if viewDic is not None and isinstance(viewDic,dict):
                return viewDic
        return viewDic

    def getSubFactoryWithId(self,viewId:str):
        resultFactory = self.subFactoryDic.get(viewId,None)
        if resultFactory is not None:
            return resultFactory
        if resultFactory is None:
            for key, item in self.subFactoryDic.items():
                resultFactory = item.getSubFactoryWithId(viewId)
                if resultFactory is not None:
                    return resultFactory
        return None

    def viewMImportAppend(self):
        viewMImportAppend:str = ''
        for key,view in self.subViews.items():
            propertyType = view.type
            if propertyType == IStatic.IOS_TEMPLATE_JSON_UILabelKey:
                continue
            if propertyType == IStatic.IOS_TEMPLATE_JSON_UIButtonKey:
                continue
            if propertyType == IStatic.IOS_TEMPLATE_JSON_UIImageViewKey:
                continue
            if propertyType == IStatic.IOS_TEMPLATE_JSON_UIViewKey:
                continue
            if propertyType == IStatic.IOS_TEMPLATE_JSON_ViewKey:
                continue
            viewMImportAppend = view.import_class_str(did_imporrt_str=viewMImportAppend)

        return viewMImportAppend

    def viewPropertyAppend(self):
        propertyList: list = []
        if self.superFactory is not None:
            propertyCode = self.view.property()
            if IStatic.str_is_empty(propertyCode) == False:
                propertyList.append(propertyCode)
        for key,subFactory in self.subFactoryDic.items():
            propertyList += subFactory.viewPropertyAppendList
        return propertyList

    def viewApiSetterAppend(self):
        viewApiSetterAppendList: list = []
        if self.superFactory is not None:
            propertySetCode = self.view.api_set_codes()
            if IStatic.str_is_empty(propertySetCode) == False:
                viewApiSetterAppendList.append(propertySetCode)
        for key,subFactory in self.subFactoryDic.items():
            viewApiSetterAppendList += subFactory.viewApiSetterAppendList
        return viewApiSetterAppendList

    def viewAddSubViewAppend(self):
        viewAddSubViewAppendList: list = []
        if self.superFactory is not None:
            moveToSuperViewCode = self.view.move_to_super_view(self.superFactory().view.propertyName)
            if IStatic.str_is_empty(moveToSuperViewCode) == False:
                viewAddSubViewAppendList.append(moveToSuperViewCode)
        for key,subFactory in self.subFactoryDic.items():
            viewAddSubViewAppendList += subFactory.viewAddSubViewAppendList
        return viewAddSubViewAppendList

    def viewGetterAndSetterAppend(self):
        viewGetterAndSetterAppendList: list = []
        if self.superFactory is not None:
            lazyLoadCode = self.view.lazy_load()
            if IStatic.str_is_empty(lazyLoadCode) == False:
                viewGetterAndSetterAppendList.append(lazyLoadCode)
        for key,subFactory in self.subFactoryDic.items():
            viewGetterAndSetterAppendList += subFactory.viewGetterAndSetterAppendList
        return viewGetterAndSetterAppendList

    def viewConstaintsAppend(self) -> []:
        viewConstaintsAppend: [str] = []
        if self.superFactory is not None:
            viewConstaintsAppend.append(self.constraintsMaker.constaintResultStr)
        for key,subFactory in self.subFactoryDic.items():
            viewConstaintsAppend += subFactory.viewConstaintsAppendList
        return viewConstaintsAppend

    def viewModelPropertyAppendNameList(self):
        viewModelPropertyAppend: [str] = []
        viewModelPropertyAppend += self.view.api_name_list
        for key,subFactory in self.subFactoryDic.items():
            viewModelPropertyAppend += subFactory.viewModelPropertyNameList
        return viewModelPropertyAppend

    def reloadAppendStrs(self):
        self.viewMImportAppendStr = self.viewMImportAppend()
        self.viewPropertyAppendList = self.viewPropertyAppend()
        self.viewApiSetterAppendList = self.viewApiSetterAppend()
        self.viewAddSubViewAppendList = self.viewAddSubViewAppend()
        self.viewGetterAndSetterAppendList = self.viewGetterAndSetterAppend()
        self.viewModelPropertyNameList = self.viewModelPropertyAppendNameList()
        self.viewConstaintsAppendList = self.viewConstaintsAppend()


if __name__ == '__main__':
    '''
    主函数：程序入口
    '''
    # path = input('请输入XIB路径:')


