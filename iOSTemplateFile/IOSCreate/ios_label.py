# 导入模块
import iOSTemplateFile.IOSCreate.ios_static_string as IStatic
from iOSTemplateFile.IOSCreate.ios_base_text import ios_base_text as base_text_view
import socket
import datetime
class ios_label(base_text_view):

    def append_lazy_load_set_propertys(self) -> [str]:
        list:[str] = super(ios_label, self).append_lazy_load_set_propertys()

        if self.text_color.is_net_api_color() == False and self.text_color.is_empty() == False:
            s = f'_{self.name}.textColor = {self.text_color.color()}';
            self.append_content(s,list)

        if self.font.is_empty() == False:
            s = f'_{self.name}.font = {self.font.font()};'
            self.append_content(s,list)

        if IStatic.str_is_empty(self.text_alignment_name) == False:
            s = f'{self.self_ivr_getter()}.textalignment = {self.text_alignment_name};'
            self.append_content(s,list)

        return list

    def set_title(self):
        return f'{self.self_getter()}.text = {self.datasource_getter()}.{self.title};'

    def append_set_property_data(self):
        list:[str] = []
        list.append(self.set_title())
        return list