# 导入模块
from iOSTemplateFile.IOSCreate.ios_base_view import ios_base_view
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic
from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_image import ios_image as IImage
import socket
import datetime
PropertyUIImageViewKey = "@property (nonatomic,strong) UIImageView *"
class ios_image_view(ios_base_view):
    image_url: str = ''
    image_name: str = ''
    image:IImage
    def __init__(self,
                 self_holder_pointer_name: str,
                 type: str,
                 name: str,
                 datasource: str,
                 datasource_holder_pointer_name: str,
                 background_color: str = '',
                 border_color: str = '',
                 border_width: str = '',
                 corner_radius: str = '',
                 masks_to_bounds: bool = False,
                 image_url: str = '',
                 image_name:str =''
                 ):
        super().__init__(
            self_holder_pointer_name=self_holder_pointer_name,
            type=type,
            name=name,
            datasource=datasource,
            datasource_holder_pointer_name=datasource_holder_pointer_name,
            background_color=background_color,
            border_color=border_color,
            border_width=border_width,
            corner_radius=corner_radius,
            masks_to_bounds=masks_to_bounds,
        )
        self.image_url = image_url
        self.image_name = image_name
        self.image = IImage(image_url=image_url,image_name=image_name)

    def append_lazy_load_set_propertys(self) -> [str]:
        list: [str] = super(ios_image_view, self).append_lazy_load_set_propertys()

        if IStatic.str_is_empty(self.image_name) == False:
            s = f'{self.self_ivr_getter()}.image = {self.text_color.color()}';
            self.append_content(s, list)

        if self.font.is_empty() == False:
            s = f'_{self.name}.font = {self.font.font()};'
            self.append_content(s, list)
        return list

    def set_imageURL(self):
        if IStatic.str_is_empty(self.image_url):
            return ''
        return f'[self.{self.name} sd_setImageWithURL: [NSURL URLWithString: {self.datasource}.{self.image_url}]];'

    def set_lazy_image_name(self):
        if IStatic.str_is_empty(self.image_name):
            return ''
        return f'{self.self_ivr_getter()}.image = {self.image.image()};'

    def append_lazy_load_set_propertys(self) -> [str]:
        list = super(ios_image_view,self).append_lazy_load_set_propertys()
        self.append_content(self.set_lazy_image_name(),list)
        return list

    def append_append_set_property_data(self):
        list: [str] = []
        list.append(self.set_imageURL())
        return '\n'.join(list)