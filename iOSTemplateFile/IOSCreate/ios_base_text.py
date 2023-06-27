
from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_font import  ios_font as IFont
from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_color import  ios_color as IColor
from iOSTemplateFile.IOSCreate.ios_base_view import  ios_base_view as base_view
from iOSTemplateFile.IOSCreate import  ios_static_string as IStatic

class ios_base_text(base_view):
    font:IFont
    text_color:IColor
    title: str = ''
    text_alignment_name:str = ''

    #api
    api_textColor: str = ''
    api_text: str = ''

    def reloadPropertys(self):
        self.text_alignment_name = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_TextAlignment,
                                             IStatic.IOS_TEMPLATE_NSTextAlignmentLeft)
        font_family = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_FontFamily, '')
        font_family_name = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_FontFamilyName, '')
        font_size = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_FontSize, '')
        text_color = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_TextColor, '')
        self.title = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_textAPI, '')

        self.font = IFont(font_family,font_family_name, font_size)
        self.text_color = IColor(color=text_color,
                                 datasource=self.datasource,
                                 datasource_holder=self.datasource_holder_pointer_name)

    def apiNames(self) -> [str]:
        arr:[str] = []
        self.api_textColor = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_textColorAPI, '')
        self.api_text = self.jsonDic.get(IStatic.IOS_TEMPLATE_JSON_textAPI, '')
        self.appendAPINameStrIfNotEmpty(arr, IStatic.IOS_TEMPLATE_JSON_textColorAPI)
        self.appendAPINameStrIfNotEmpty(arr, IStatic.IOS_TEMPLATE_JSON_textAPI)
        return arr


