# 导入模块
import os
import socket
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic
from iOSTemplateFile.IOSCreate.ios_base_text import ios_base_text as base_text_view

class ios_button(base_text_view):

    def set_title(self):
        return None
        if self.title is None:
            return ''
        return f'''
        [{self.self_getter()} setTitle: {self.datasource_getter()}.{self.title} forState: UIControlStateNormal];
        '''.lstrip()

    def lazy_load(self):
        str = super(ios_button, self).lazy_load()
        str += f'''
        - (void)click_{self.name} {{
        
        }}
        '''.strip()
        return str

    def append_lazy_load_set_propertys(self) -> [str]:
        list: [str] = super(ios_button, self).append_lazy_load_set_propertys()

        if self.text_color.is_net_api_color() == False and self.text_color.is_empty() == False:
            s = f'[{self.self_ivr_getter()} setTitleColor:{self.text_color.color()} forState:UIControlStateNormal];'
            self.append_content(s, list)

        if self.font.is_empty() == False:
            s = f'{self.self_ivr_getter()}.titleLabel.font = {self.font.font()};'
            self.append_content(s, list)
        append_str = f'''
            [_{self.name} addTarget:self action:@selector(click_{self.name}) forControlEvents:UIControlEventTouchUpInside];
        '''.strip()
        list.append(append_str)
        return list

    def append_set_property_data(self) -> [str]:
        list:[str] = []
        list.append(self.set_title())
        return list


