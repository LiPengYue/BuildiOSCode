from iOSTemplateFile.IOSCreate.ios_view_base_data import ios_color as IColor
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic

class ios_view_model:
    savePath:str
    name:str
    baseViewModelName:str = ''
    viewModelName:str = ''

    template_baseViewModelName: str = ''
    template_viewModelName: str = ''

    template_viewModelH_FileName:str = ''
    template_viewModelM_FileName:str = ''

    propertys:[str] = []

    def __init__(self,
                 baseViewModelName: str,
                 viewModelName: str,
                 template_baseViewModelName,
                 template_viewModelName,
                 template_viewModelH_FileName,
                 template_viewModelM_FileName,
                 ):
        self.baseViewModelName = baseViewModelName
        self.viewModelName = viewModelName
        self.template_baseViewModelName = template_baseViewModelName
        self.template_viewModelName = template_viewModelName
        self.template_viewModelH_FileName = template_viewModelH_FileName
        self.template_viewModelM_FileName = template_viewModelM_FileName

    def add_color_property_ifNeeded(self,color:str):
        if IColor.is_net_api_color(color) == False:
            return
        color_property =  f'{IStatic.IOS_TEMPLATE_PROPERTY_copy} {IStatic.IOS_TEMPLATE_TYPE_NSString} *{color};'
        self.__append_property(color_property)

    def add_property(self,property_name:str):
        if IStatic.str_is_empty(property_name):
            return
        property = f'{IStatic.IOS_TEMPLATE_PROPERTY_copy} {IStatic.IOS_TEMPLATE_TYPE_NSString} *{property_name};'
        self.__append_property(property)

    def __append_property(self, constraint: str):
        if len(constraint) == 0:
            return
        constraint = constraint
        if constraint[-1] != ';':
            constraint += ';'
        self.propertys.append(constraint)

    def get_properts(self):
        return '\n'.join(self.propertys)
