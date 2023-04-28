import re
#用户配置
IOS_TEMPLATE_UserName = 'template_userNameKey'
IOS_TEMPLATE_NickName = 'template_nickNameKey'
IOS_TEMPLATE_ProjectName = 'template_projectNameKey'


#chars
IOS_TEMPLATE_char_newline = '\n'
IOS_TEMPLATE_char_colon = ':'
IOS_TEMPLATE_char_bracket_left = '{'
IOS_TEMPLATE_char_bracket_right = '}'
IOS_TEMPLATE_char_parentheses_left = '('
IOS_TEMPLATE_char_parentheses_right = ')'
IOS_TEMPLATE_char_space = ' '
IOS_TEMPLATE_char_tab = IOS_TEMPLATE_char_space * 4


#Parma 导入相关
IOS_TEMPLATE_TYPE_Import = '#import'
#导入UIKit
IOS_TEMPLATE_TYPE_Import_UIKit = '\n{IOS_TEMPLATE_TYPE_Import} <UIKit/UIKit.h>'.format(IOS_TEMPLATE_TYPE_Import = IOS_TEMPLATE_TYPE_Import)


# implementation && interface
IOS_TEMPLATE_Protocol = '@protocol'
IOS_TEMPLATE_Protocol_base_delegate = '<NSObject>'
IOS_TEMPLATE_Interface = '@interface'
IOS_TEMPLATE_Implementation = '@implementation'
IOS_TEMPLATE_End = '@end'

IOS_TEMPLATE_PROPERTY_strong = '@property (nonatomic,strong)'
IOS_TEMPLATE_PROPERTY_copy = '@property (nonatomic,copy)'
IOS_TEMPLATE_PROPERTY_assign = '@property (nonatomic,assign)'

IOS_TEMPLATE_TYPE_Class = 'Class'
IOS_TEMPLATE_TYPE_UITableViewView = 'UITableViewView'
IOS_TEMPLATE_TYPE_UILabel = 'UILabel'
IOS_TEMPLATE_TYPE_UIButton = 'UIButton'
IOS_TEMPLATE_TYPE_UIImageView = 'UIImageView'
IOS_TEMPLATE_TYPE_NSString = 'NSString'
IOS_TEMPLATE_TYPE_NSInteger = 'NSInteger'
IOS_TEMPLATE_TYPE_CGFloat = 'CGFloat'
IOS_TEMPLATE_TYPE_BOOL = 'BOOL'
IOS_TEMPLATE_TYPE_NSNumber = 'NSNumber'
IOS_TEMPLATE_TYPE_NSArray = 'NSArray'
IOS_TEMPLATE_TYPE_NSObject = 'NSObject'

#constraints
IOS_TEMPLATE_NSTextAlignmentLeft = 'NSTextAlignmentLeft'
IOS_TEMPLATE_NSTextAlignmentCenter = 'NSTextAlignmentCenter'
IOS_TEMPLATE_NSTextAlignmentRight = 'NSTextAlignmentRight'

#json 解析
#事例
'''
{"template_projectNameKey":"自动生成器","template_userNameKey":"template_userNameKey","template_nickNameKey":"template_userNameKey","viewName":"ZRKeeperCustomerServiceCenterSearchview","ViewModelName":"ZRKeeperCustomerServiceCenterSearchViewModel","SavePathKey":"/Users/lp1/01我的文件/一些资料/code/demo","BaseViewModelName":"ZRKeeperCustomerServiceCenterBaseViewModel","SavePath":"/Users/lp1/01我的文件/一些资料/code/demo","SubViews":[{"PropertyType":"UILabel","PropertyName":"titleLabel","APINameKey":"title","Constraints":{"SuperView":"","ConstraintView_Top":"","ConstraintSpace_Top":"12","ConstraintView_Left":"","ConstraintSpace_Left":"12","ConstraintView_Bottom":"","ConstraintSpace_Bottom":"-12","ConstraintView_Right":"","ConstraintSpace_Right":"-12","Constraint_height":"120","Constraint_width":"110"}},{"PropertyType":"UILabel","PropertyName":"subtitleLabel","APINameKey":"subtitle","Constraints":{"SuperView":"","ConstraintView_Top":"","ConstraintSpace_Top":"12","ConstraintView_Left":"","ConstraintSpace_Left":"12","ConstraintView_Bottom":"","ConstraintSpace_Bottom":"-12","ConstraintView_Right":"","ConstraintSpace_Right":"-12"}},{"PropertyType":"UIImageView","PropertyName":"bgImageView","APINameKey":"bgImage"},{"PropertyType":"UIButton","PropertyName":"bgButton","APINameKey":"buttonText"}]}
'''
IOS_TEMPLATE_JSON_PropertyTypeKey = 'PropertyType'
IOS_TEMPLATE_JSON_PropertyNameKey = 'PropertyName'
IOS_TEMPLATE_JSON_DataSouceName = 'DataSouceName'

IOS_TEMPLATE_JSON_UILabelKey = 'UILabel'
IOS_TEMPLATE_JSON_UIImageViewKey = 'UIImageView'
IOS_TEMPLATE_JSON_UIButtonKey = 'UIButton'

IOS_TEMPLATE_JSON_BorderColorKey = 'BorderColor'
IOS_TEMPLATE_JSON_TextColorKey = 'TextColor'
IOS_TEMPLATE_JSON_BackgroundColorKey = 'BackgroundColor'
IOS_TEMPLATE_JSON_BorderWidthKey = 'BorderWidth'
IOS_TEMPLATE_JSON_CornerRadiusKey = 'CornerRadius'
IOS_TEMPLATE_JSON_MasksToBoundsKey = 'MasksToBounds'

IOS_TEMPLATE_JSON_MasksTo_FontFamily = 'FontFamily'
IOS_TEMPLATE_JSON_MasksTo_TextAlignment = 'TextAlignment'
IOS_TEMPLATE_JSON_MasksTo_FontSize = 'FontSize'
IOS_TEMPLATE_JSON_MasksTo_TextColor = 'TextColor'
IOS_TEMPLATE_JSON_MasksTo_ImageName = 'ImageName'


IOS_TEMPLATE_JSON_APINameKey = "APINameKey"#view的值取自 json中的APINameKey

IOS_TEMPLATE_JSON_ViewNameKey = 'ViewName'
IOS_TEMPLATE_JSON_ViewModelKey = 'ViewModelName'
IOS_TEMPLATE_JSON_BaseViewModelKey = 'BaseViewModelName'
IOS_TEMPLATE_JSON_SavePathKey = 'SavePath'
IOS_TEMPLATE_JSON_SubViewsKey = 'SubViews'

def str_is_empty(string:str):
    return str is None or isinstance(string,str) == False or len(string) == 0

def str_is_url(string:str):
    return re.match(r'^https?:/{2}\w.+$', string)