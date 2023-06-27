# 导入模块
import iOSTemplateFile.IOSCreate.ios_static_string as IStatic
from iOSTemplateFile.IOSCreate.ios_base_text import ios_base_text as base_text_view
from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_color import ios_color as IColor

import socket
import datetime
class ios_label(base_text_view):

    def append_lazy_load_set_propertys(self) -> [str]:
        list:[str] = super(ios_label, self).append_lazy_load_set_propertys()

        if self.text_color.is_empty() == False:
            s = f'_{self.propertyName}.textColor = {self.text_color.color()}';
            self.array_append_content(s,list)

        if self.font.is_empty() is False:
            fontStr = self.font.font()
            s = f'_{self.propertyName}.font = {fontStr};'
            self.array_append_content(s,list)

        if IStatic.str_is_empty(self.text_alignment_name) == False:
            s = f'{self.self_ivr_getter()}.textalignment = {self.text_alignment_name};'
            self.array_append_content(s,list)

        return list

    def api_set_title(self):
        return f'{self.self_getter()}.text = {self.api_set_viewModelPropertyGetter(self.api_text)};'

    def api_set_titleColor(self):
        if IStatic.str_is_empty(self.api_textColor):
            return ''
        color = IColor(self.api_textColor,
                       datasource_holder=self.datasource_holder_pointer_name,
                       datasource=self.datasource)
        return f'''
                  {self.self_getter()}.textColor = {color.color()};
                  '''.lstrip()

    def api_set_append_property_datas(self):
        list:[str] = []
        list.append(self.api_set_title())
        list.append(self.api_set_titleColor())
        return list