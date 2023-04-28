import iOSTemplateFile.IOSCreate.ios_static_string as IStatic
class ios_image:
    image_url:str
    image_name:str = ''

    def __init__(self,image_url:str='',image_name:str = ''):
        self.image_name = image_name
        self.image_url = image_url

    def is_url(self):
        return IStatic.str_is_url(self.image_url)

    def image(self):
        if IStatic.str_is_empty(self.image_name):
            return ''
        return f'[ZRImage imageNamed:@"{self.image_name}"]'
