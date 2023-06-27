import re
import os.path
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

#NSTextAlignment
IOS_TEMPLATE_NSTextAlignmentLeft = 'NSTextAlignmentLeft'
IOS_TEMPLATE_NSTextAlignmentCenter = 'NSTextAlignmentCenter'
IOS_TEMPLATE_NSTextAlignmentRight = 'NSTextAlignmentRight'

#constraints
IOS_TEMPLATE_JSON_Constraints = 'constraints'
IOS_TEMPLATE_JSON_Constraint = 'constraint'
IOS_TEMPLATE_JSON_FirstItem = 'firstItem'
IOS_TEMPLATE_JSON_FirstAttribute = 'firstAttribute'
IOS_TEMPLATE_JSON_SecondItem = 'secondItem'
IOS_TEMPLATE_JSON_SecondAttribute = 'secondAttribute'
IOS_TEMPLATE_JSON_Constant = 'constant'
IOS_TEMPLATE_JSON_Id = 'id'
IOS_TEMPLATE_JSON_Priority = 'priority'
IOS_TEMPLATE_JSON_Symbolic = 'symbolic'
IOS_TEMPLATE_JSON_Relation = 'relation'

#json 解析
#事例
'''
{"template_projectNameKey":"自动生成器","template_userNameKey":"template_userNameKey","template_nickNameKey":"template_userNameKey","viewName":"ZRKeeperCustomerServiceCenterSearchview","ViewModelName":"ZRKeeperCustomerServiceCenterSearchViewModel","SavePathKey":"/Users/lp1/01我的文件/一些资料/code/demo","BaseViewModelName":"ZRKeeperCustomerServiceCenterBaseViewModel","SavePath":"/Users/lp1/01我的文件/一些资料/code/demo","SubViews":[{"PropertyType":"UILabel","PropertyName":"titleLabel","APINameKey":"title","Constraints":{"SuperView":"","ConstraintView_Top":"","ConstraintSpace_Top":"12","ConstraintView_Left":"","ConstraintSpace_Left":"12","ConstraintView_Bottom":"","ConstraintSpace_Bottom":"-12","ConstraintView_Right":"","ConstraintSpace_Right":"-12","Constraint_height":"120","Constraint_width":"110"}},{"PropertyType":"UILabel","PropertyName":"subtitleLabel","APINameKey":"subtitle","Constraints":{"SuperView":"","ConstraintView_Top":"","ConstraintSpace_Top":"12","ConstraintView_Left":"","ConstraintSpace_Left":"12","ConstraintView_Bottom":"","ConstraintSpace_Bottom":"-12","ConstraintView_Right":"","ConstraintSpace_Right":"-12"}},{"PropertyType":"UIImageView","PropertyName":"bgImageView","APINameKey":"bgImage"},{"PropertyType":"UIButton","PropertyName":"bgButton","APINameKey":"buttonText"}]}
'''
IOS_TEMPLATE_JSON_PropertyTypeKey = 'propertyType'
IOS_TEMPLATE_JSON_PropertyNameKey = 'propertyName'
IOS_TEMPLATE_JSON_DataSouceName = 'dataSouceName'

IOS_TEMPLATE_JSON_UILabelKey = 'UILabel'
IOS_TEMPLATE_JSON_UIImageViewKey = 'UIImageView'
IOS_TEMPLATE_JSON_UIButtonKey = 'UIButton'
IOS_TEMPLATE_JSON_ViewKey = 'view'
IOS_TEMPLATE_JSON_UIViewKey = 'UIView'

IOS_TEMPLATE_JSON_BorderColorKey = 'borderColor'
IOS_TEMPLATE_JSON_TextColorKey = 'textColor'
IOS_TEMPLATE_JSON_BackgroundColorKey = 'backgroundColor'
IOS_TEMPLATE_JSON_BorderWidthKey = 'borderWidth'
IOS_TEMPLATE_JSON_CornerRadiusKey = 'cornerRadius'
IOS_TEMPLATE_JSON_MasksToBoundsKey = 'masksToBounds'
#userinterfaceAttributes
IOS_TEMPLATE_JSON_UserDefinedRuntimeAttributes = 'userDefinedRuntimeAttributes'
IOS_TEMPLATE_JSON_UserAttributesKey = 'userAttributesKey'
IOS_TEMPLATE_JSON_UserAttributesKeyPath = 'userAttributesKeyPath'
IOS_TEMPLATE_JSON_UserAttributesValue = 'userAttributesValue'
IOS_TEMPLATE_JSON_UserAttributesType = 'userAttributesType'
IOS_TEMPLATE_JSON_UserAttributesReal = 'userAttributesReal'


IOS_TEMPLATE_JSON_FontFamily = 'fontFamily'
IOS_TEMPLATE_JSON_FontFamilyName = 'fontFamilyName'
IOS_TEMPLATE_JSON_TextAlignment = 'textAlignment'
IOS_TEMPLATE_JSON_FontSize = 'fontSize'
IOS_TEMPLATE_JSON_TextColor = 'textColor'
IOS_TEMPLATE_JSON_ImageName = 'imageName'

IOS_TEMPLATE_JSON_NodeId = 'nodeId'

IOS_TEMPLATE_JSON_APINameKey = "APINameKey"#view的值取自 json中的APINameKey
IOS_TEMPLATE_JSON_textColorAPI = "textColorAPI"#view的值取自 json中的APINameKey
IOS_TEMPLATE_JSON_textAPI = "textAPI"#view的值取自 json中的APINameKey
IOS_TEMPLATE_JSON_imageAPI = "imageAPI"
IOS_TEMPLATE_JSON_bgColorAPI = 'bgColorAPI'

IOS_TEMPLATE_JSON_ViewNameKey = 'viewName'
IOS_TEMPLATE_JSON_ViewModelKey = 'viewModelName'
IOS_TEMPLATE_JSON_BaseViewModelKey = 'baseViewModelName'
IOS_TEMPLATE_JSON_SavePathKey = 'savePath'
IOS_TEMPLATE_JSON_SubViewsKey = 'subViews'

# 从根目录下开始获取其他路径
# 获得根路径
def getRootPath():
    # 获取文件目录
    curPath = os.path.abspath(os.path.dirname(__file__))
    # 获取项目根路径，内容为当前项目的名字
    rootPath = curPath[:curPath.find('BuildiOSCode') + len('BuildiOSCode')]
    return rootPath

def getOtherPath(abspath:str):
	# 调用了上述获得项目根目录的方法
    rootPath = getRootPath()
    dataPath = os.path.abspath(rootPath + abspath)
    return dataPath

def str_is_empty(string:str):
    return str is None or isinstance(string,str) == False or len(string) == 0

def str_is_not_empty(string:str):
    empty = str_is_empty(string)
    return empty == False

def str_is_url(string:str):
    return re.match(r'^https?:/{2}\w.+$', string)

def path(path:str) -> str:
    return f"\"{path}\""