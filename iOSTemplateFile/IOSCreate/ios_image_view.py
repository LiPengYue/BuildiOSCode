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

    api_image:str = ''

    def reloadPropertys(self):
        self.image_url = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_imageAPI,"")
        self.image_name = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_ImageName,'')
        self.image = IImage(image_url=self.image_url, image_name=self.image_name)

    def append_lazy_load_set_propertys(self) -> [str]:
        list: [str] = super(ios_image_view, self).append_lazy_load_set_propertys()

        if IStatic.str_is_empty(self.image_name) == False:
            s = f'{self.self_ivr_getter()}.image = {self.image.image()}'
            self.array_append_content(s, list)
        return list

    def set_imageURL(self):
        if IStatic.str_is_empty(self.image_url):
            return ''
        return f'[self.{self.propertyName} sd_setImageWithURL: [NSURL URLWithString: {self.datasource}.{self.image_url}]];'

    def append_append_set_property_data(self):
        list: [str] = []
        list.append(self.set_imageURL())
        return '\n'.join(list)

    def apiNames(self) -> [str]:
        arr:[str] = []
        self.api_image = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_imageAPI, '')
        self.appendAPINameStrIfNotEmpty(arr, IStatic.IOS_TEMPLATE_JSON_imageAPI)
        return arr

    def api_set_append_property_datas(self) -> [str]:
        arr = []
        self.array_append_content(self.api_set_image(),arr)
        return arr

    def api_set_image(self):
        if IStatic.str_is_empty(self.api_image):
            return ''

        return f'''
                [{self.self_getter()} sd_setImageWithURL:[NSURL URLWithString:{self.api_set_viewModelPropertyGetter(self.api_image)}?:@""]];
                '''.lstrip()