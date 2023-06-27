import re
import weakref
from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_color import ios_color as IColor
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic

IOS_Regular_Lazy_set = 'IOS_Regular_Lazy_set'

class ios_base_view:

    #用于拼接赋值属性的 ViewModel
    datasource:str = ''
    # ViewModel所有者指针的指针名
    datasource_holder_pointer_name: str = 'self'

    #唯一标识
    id: str = ''
    #属性名
    propertyName:str = ''
    #self 视图 类型
    type: str = ''
    #self所有者指针的指针名
    self_holder_pointer_name:str = 'self'

    #self的基础属性
    background_color: str = ''
    border_color: str = ''
    border_width: str = ''
    corner_radius: str = ''
    masks_to_bounds: bool = False

    #viewModel API
    bgColorAPI: str = ''

    api_image: str = ''

    jsonDic: dict = {}

    subviews:list = []
    api_name:str = ''
    api_name_list: [str] = []
    superView:weakref = None

    def __init__(self,
                 self_holder_pointer_name:str,
                 datasource:str,
                 datasource_holder_pointer_name:str,
                 jsonDic:dict
                 ):

        self.datasource = datasource
        self.self_holder_pointer_name = self_holder_pointer_name
        self.datasource_holder_pointer_name = datasource_holder_pointer_name

        self.jsonDic = jsonDic
        self.__reloadPropertys()
        self.api_name_list = self.__apiNames()

    def __reloadPropertys(self):
        self.id = self.jsonDic[IStatic.IOS_TEMPLATE_JSON_NodeId]
        if IStatic.str_is_empty(self.id):
            self.id = self.jsonDic[IStatic.IOS_TEMPLATE_JSON_NodeId]
        self.type = self.jsonDic[IStatic.IOS_TEMPLATE_JSON_PropertyTypeKey]
        self.propertyName = self.jsonDic[IStatic.IOS_TEMPLATE_JSON_PropertyNameKey]
        self.background_color = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_BackgroundColorKey, '')
        self.border_color = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_BorderColorKey, '')
        self.border_width  = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_BorderWidthKey, '')
        self.corner_radius = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_CornerRadiusKey, '')
        self.masks_to_bounds = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_MasksToBoundsKey, '')
        self.api_name = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_APINameKey, '')
        self.reloadPropertys()

    def reloadPropertys(self):
        pass

    def property(self):
        return f'@property (nonatomic,strong) {self.type} *{self.propertyName};'

    def self_getter(self):
        return f'''{self.self_holder_pointer_name}.{self.propertyName}'''

    def self_ivr_getter(self):
        return f'''_{self.propertyName}'''

    def datasource_getter(self):
        return f'{self.datasource_holder_pointer_name}.{self.datasource}'

    def move_to_super_view(self, superview_name: str = '') -> str:
        str = f'[{self.self_holder_pointer_name}'

        if IStatic.str_is_empty(superview_name) == False:
            str += ('.'+superview_name)
        str += f' addSubview:self.{self.propertyName}];'
        return str

    def import_class_str(self,did_imporrt_str:str='') -> str:
        str = ''
        import_colass = f'#import "{self.type}.h"'
        if import_colass in did_imporrt_str:
            str = did_imporrt_str
        else:
            str = did_imporrt_str + import_colass + '\n'
        return str

    # lazys
    def lazy_load(self):
        str = f'''
         - ({self.type} *) {self.propertyName} {{
             if (!_{self.propertyName}) {{
                 _{self.propertyName} = [[{self.type} alloc]init];
                 {IOS_Regular_Lazy_set}
             }}
             return _{self.propertyName};
         }}'''
        re_regular_Lazy_set = re.search(IOS_Regular_Lazy_set, str, flags=re.DOTALL)
        front = str[:re_regular_Lazy_set.start()]
        last = str[re_regular_Lazy_set.end():]
        append = '\n'.join(self.get_lazy_load_set_propertys_str())
        str = front + append + last
        return str

    def lazy_set_backgroundColor(self):
        if IStatic.str_is_empty(self.background_color):
            return ''
        color = IColor(self.background_color,
                       datasource_holder=self.datasource_holder_pointer_name,
                       datasource=self.datasource)
        if color.is_net_api_color():
            return ''

        return f'''
            {self.self_ivr_getter()}.backgroundColor = {color.color()};
            '''.lstrip()

    def lazy_set_border_color(self):
        if IStatic.str_is_empty(self.border_color):
            return ''
        color = IColor(self.border_color,
                       datasource_holder=self.datasource_holder_pointer_name,
                       datasource=self.datasource)
        if color.is_net_api_color():
            return ''
        return f'''
        {self.self_ivr_getter()}.layer.borderColor = {color.color()}.CGColor;
        '''.lstrip()

    def lazy_set_border_width(self):
        if isinstance(self.border_width,str) and  IStatic.str_is_empty(self.border_width):
            return ''
        if IStatic.str_is_empty(self.border_width):
            return ''
        if float(self.border_width) <= 0:
            return ''
        return f'''
        {self.self_ivr_getter()}.layer.borderWidth = {self.border_width};
        '''.lstrip()

    def lazy_set_corner_radius(self):
        if isinstance(self.corner_radius,str) and IStatic.str_is_empty(self.corner_radius):
            return ''
        if IStatic.str_is_empty(self.corner_radius):
            return ''
        if float(self.corner_radius) <= 0:
            return ''
        return f'''
        {self.self_ivr_getter()}.layer.cornerRadius = {self.corner_radius};
        '''.lstrip()

    def lazy_set_masks_to_bounds(self):
        if isinstance(self.masks_to_bounds,str) and IStatic.str_is_empty(self.masks_to_bounds):
            return ''
        if self.masks_to_bounds is None:
            return ''
        if float(self.masks_to_bounds) <= 0:
            return ''
        return f'''
        {self.self_ivr_getter()}.layer.masksToBounds = {self.masks_to_bounds};
        '''.lstrip()

    def array_append_content(self, constraint: str, constraint_list: list):
        constraint = constraint.strip()
        if IStatic.str_is_empty(constraint):
            return
        if constraint[-1] != ';':
            constraint += ';'
        constraint_list.append(constraint)
        # print(f'---{constraint_list}')

    def insert_content(self, constraint: str, constraint_list: list,index:int):
        constraint = constraint.strip()
        if IStatic.str_is_empty(constraint):
            return
        if constraint[-1] != ';':
            constraint += ';'
        constraint_list.insert(index,constraint)


    def get_lazy_load_set_propertys_str(self) ->[str]:
        list = self.__lazy_load_set_propertys()
        list += self.append_lazy_load_set_propertys()
        return list
        
    def __lazy_load_set_propertys(self) -> [str]:
        backgroundColor = self.lazy_set_backgroundColor()
        border_color = self.lazy_set_border_color()
        border_width = self.lazy_set_border_width()
        corner_radius = self.lazy_set_corner_radius()
        masks_to_bounds = self.lazy_set_masks_to_bounds()
        list:[str] = []

        self.array_append_content(backgroundColor, list)
        self.array_append_content(border_color, list)
        self.array_append_content(border_width, list)
        self.array_append_content(corner_radius, list)
        self.array_append_content(masks_to_bounds, list)
        # print(list)
        return list

    def append_lazy_load_set_propertys(self) -> [str]:
        return []

    # -- API
    def apiNames(self) -> [str]:
        pass

    def __apiNames(self) -> [str]:
        arr = []
        self.api_name = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_APINameKey, '')
        self.bgColorAPI = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_bgColorAPI, '')

        self.appendAPINameStrIfNotEmpty(arr, IStatic.IOS_TEMPLATE_JSON_APINameKey)
        self.appendAPINameStrIfNotEmpty(arr, IStatic.IOS_TEMPLATE_JSON_bgColorAPI)

        moreAPINames = self.apiNames()
        if isinstance(moreAPINames, list):
            arr += moreAPINames
        return arr

    def appendAPINameStrIfNotEmpty(self, arr: [], key: str):
        if IStatic.str_is_empty(key):
            return
        name = self.jsonDic.get(key, '')
        if IStatic.str_is_empty(name):
            return
        arr.append(name)

    #api set
    def api_set_codes(self):
        list = self.__api_set_base_property_data()
        str = ''
        if len(list) > 0:
            str += f'// {self.propertyName}{IStatic.IOS_TEMPLATE_char_newline}'
        str += '\n'.join(list)
        return str

    def __api_set_base_property_data(self) -> [str]:
        list: [str] = []
        background_color = self.api_set_backgroundColor()
        self.array_append_content(background_color,list)
        self.array_append_content(self.api_name, list)
        list += self.api_set_append_property_datas()
        return list

    def api_set_viewModelPropertyGetter(self,propertyName:str) -> str:
        if IStatic.str_is_empty(propertyName):
            return ''
        return f'{self.datasource_getter()}.{propertyName}'

    def api_set_backgroundColor(self):
        if IStatic.str_is_empty(self.bgColorAPI):
            return ''

        return f'''
               {self.self_getter()}.{IStatic.IOS_TEMPLATE_JSON_BackgroundColorKey} = {self.api_set_viewModelPropertyGetter(self.bgColorAPI)};
               '''.lstrip()

    def api_set_append_property_datas(self) -> [str]:
        return []