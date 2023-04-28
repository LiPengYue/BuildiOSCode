import re

from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_color import ios_color as IColor
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic

IOS_Regular_Lazy_set = 'IOS_Regular_Lazy_set'

class ios_base_view:

    #用于拼接赋值属性的 ViewModel
    datasource:str = ''
    # ViewModel所有者指针的指针名
    datasource_holder_pointer_name: str = 'self'

    #属性名
    name:str = ''
    #self 视图 类型
    type: str = ''
    #self所有者指针的指针名
    self_holder_pointer_name:str = 'self'

    #viewModel的属性
    background_color: str = ''
    border_color: str = ''
    border_width: str = ''
    corner_radius: str = ''
    masks_to_bounds: bool = False

    def __init__(self,
                 self_holder_pointer_name:str,
                 type:str,
                 name:str,
                 datasource:str,
                 datasource_holder_pointer_name:str,
                 background_color: str = '',
                 border_color: str = '',
                 border_width: str = '',
                 corner_radius: str = '',
                 masks_to_bounds: bool = False
                 ):

        self.name = name
        self.type = type
        self.datasource = datasource
        self.self_holder_pointer_name = self_holder_pointer_name
        self.datasource_holder_pointer_name = datasource_holder_pointer_name

        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.corner_radius = corner_radius
        self.masks_to_bounds = masks_to_bounds

    def property(self):
        return f'@property (nonatomic,strong) {self.type} *{self.name};'

    def self_getter(self):
        return f'''{self.self_holder_pointer_name}.{self.name}'''

    def self_ivr_getter(self):
        return f'''_{self.name}'''

    def datasource_getter(self):
        return f'{self.datasource_holder_pointer_name}.{self.datasource}'

    def move_to_super_view(self, superview_name: str = '') -> str:
        str = f'[{self.self_holder_pointer_name}'

        if IStatic.str_is_empty(superview_name) == False:
            str += ('.'+superview_name)
        str += f' addSubview:self.{self.name}];'
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
         - ({self.type} *) {self.name} {{
             if (!_{self.name}) {{
                 _{self.name} = [[{self.type} alloc]init];
                 {IOS_Regular_Lazy_set}
             }}
             return _{self.name};
         }}
             '''
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

    def set_backgroundColor(self):
        if IStatic.str_is_empty(self.background_color):
            return ''
        color = IColor(self.background_color,
                       datasource_holder=self.datasource_holder_pointer_name,
                       datasource=self.datasource)
        if color.is_net_api_color() == False:
            return ''
        return f'''
               {self.self_getter()}.backgroundColor = {color.color()};
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
        if self.border_width is None:
            return ''
        return f'''
        {self.self_ivr_getter()}.layer.borderWidth = {self.border_width};
        '''.lstrip()

    def lazy_set_corner_radius(self):
        if isinstance(self.corner_radius,str) and IStatic.str_is_empty(self.corner_radius):
            return ''
        if self.corner_radius is None:
            return ''
        return f'''
        {self.self_ivr_getter()}.layer.cornerRadius = {self.corner_radius};
        '''.lstrip()

    def lazy_set_masks_to_bounds(self):
        if isinstance(self.masks_to_bounds,str) and IStatic.str_is_empty(self.masks_to_bounds):
            return ''
        if self.masks_to_bounds is None:
            return ''
        return f'''
        {self.self_ivr_getter()}.layer.masksToBounds = {self.masks_to_bounds};
        '''.lstrip()

    def append_content(self, constraint: str, constraint_list: list):
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

        self.append_content(backgroundColor, list)
        self.append_content(border_color, list)
        self.append_content(border_width, list)
        self.append_content(corner_radius, list)
        self.append_content(masks_to_bounds, list)
        # print(list)
        return list

    def append_lazy_load_set_propertys(self) -> [str]:
        return []

    def propertys_set_data_str(self):
        list = self.__set_base_property_data()
        str = ''
        if len(list) > 0:
            str += f'// {self.name}\n'

        for value in list:
            if IStatic.str_is_empty(value):
                continue
            value_str:str = value
            str += (value_str.lstrip() + '\n')
        return str

    def __set_base_property_data(self) -> [str]:
        background_color = self.set_backgroundColor()
        list: [str] = []
        self.append_content(background_color, list)
        list += self.append_set_property_data()
        return list

    def append_set_property_data(self) -> [str]:
        return []