
from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_font import  ios_font as IFont
from iOSTemplateFile.IOSCreate.ios_view_base_data.ios_color import  ios_color as IColor
from iOSTemplateFile.IOSCreate.ios_base_view import  ios_base_view as base_view
from iOSTemplateFile.IOSCreate import  ios_static_string as IStatic

class ios_base_text(base_view):
    font:IFont
    text_color:IColor
    title: str = ''
    text_alignment_name:str = ''
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
                 title: str = '',
                 font_family:str='',
                 font_size:str='',
                 text_color:str='',
                 text_alignment_name = IStatic.IOS_TEMPLATE_NSTextAlignmentLeft
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
        self.title = title
        self.font = IFont(font_family,font_size)
        self.text_color = IColor(color=text_color,datasource=datasource,datasource_holder=datasource_holder_pointer_name)
        self.text_alignment_name = text_alignment_name