# 导入模块
import os
import socket
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic
from iOSTemplateFile.IOSCreate.ios_base_text import ios_base_text as base_text_view
from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_color import ios_color as IColor

class ios_button(base_text_view):

    def set_title(self):
        if self.title is None:
            return ''
        return f'''
        [{self.self_getter()} setTitle: {self.datasource_getter()}.{self.title} forState: UIControlStateNormal];
        '''.lstrip()

    def lazy_load(self):
        str = super(ios_button, self).lazy_load().strip()
        str += f'''
        - (void)click_{self.propertyName} {{
        
        }}'''
        return str

    def append_lazy_load_set_propertys(self) -> [str]:
        list: [str] = super(ios_button, self).append_lazy_load_set_propertys()

        if self.text_color.is_net_api_color() == False and self.text_color.is_empty() == False:
            s = f'[{self.self_ivr_getter()} setTitleColor:{self.text_color.color()} forState:UIControlStateNormal];'
            self.array_append_content(s, list)

        if self.font.is_empty() == False:
            s = f'{self.self_ivr_getter()}.titleLabel.font = {self.font.font()};'
            self.array_append_content(s, list)

        append_str = f'''
            [_{self.propertyName} addTarget:self action:@selector(click_{self.propertyName}) forControlEvents:UIControlEventTouchUpInside];
        '''

        self.array_append_content(append_str, list)
        return list

    def append_set_property_data(self) -> [str]:
        list:[str] = []
        list.append(self.set_title())
        return list

    def api_set_append_property_datas(self) -> [str]:
        arr:[str] = []
        self.array_append_content(self.api_set_title(),arr)
        self.array_append_content(self.api_set_titleColor(), arr)
        return arr

    def api_set_title(self) -> str:
        if IStatic.str_is_empty(self.api_text):
            return ''
        return f'''
        [{self.self_getter()} setTitle: {self.api_set_viewModelPropertyGetter(self.api_text)} forState: UIControlStateNormal];
        '''.lstrip()

    def api_set_titleColor(self):
        if IStatic.str_is_empty(self.api_textColor):
            return ''
        color = IColor(self.api_textColor,
                       datasource_holder=self.datasource_holder_pointer_name,
                       datasource=self.datasource)
        return f'''
               [{self.self_getter()} setTitleColor:{color.color()} forState:UIControlStateNormal];
               '''.lstrip()