
from enum import Enum
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic

Constraints_info = 'Constraints'
Constraints_Top = 'Top'
Constraints_Left = 'Left'
Constraints_Bottom = 'Bottom'
Constraints_Right = 'Right'
Constraints_Height = 'Height'
Constraints_Width = 'Width'

Constraints_View = 'View'
Constraints_Space = 'Space'
Constraints_Location = 'Location'
_left = 'left'
_right = 'right'
_trailing = 'trailing'
_leading = 'leading'


_top = 'top'
_bottom = 'bottom'

_str_make:str = 'make'
_str_equalTo:str = 'equalTo'
_str_lessThanOrEqual:str = 'lessThanOrEqual'
_str_greaterThanOrEqualTo:str = 'greaterThanOrEqualTo'


class ios_constaint_item:
    # constraints

    constantResultStr:str = ''

    viewId = ''
    constraints = ''
    constraint = ''
    firstItemId = ''
    firstItemName = ''
    firstAttribute = ''
    firstOriginAttribute = ''
    secondItemId = ''
    secondItemName = ''
    secondAttribute = ''
    secondOriginAttribute = ''
    constant = ''
    id = ''
    priority = ''
    symbolic = ''
    relation = ''

    # 定义修饰器
    def getViewOwnerNameCallback(self, func):
        self.getViewOwnerNameCallback_func = func

    def __init__(self,constaintMap:dict,viewId:str):
        self.viewId = viewId
        self.constraint = constaintMap.get(IStatic.IOS_TEMPLATE_JSON_Constraint, '')
        self.relationOrigin = constaintMap.get(IStatic.IOS_TEMPLATE_JSON_Relation, '')
        self.setupRelation()
        self.firstItemId = constaintMap.get(IStatic.IOS_TEMPLATE_JSON_FirstItem, '')
        self.firstOriginAttribute = constaintMap.get(IStatic.IOS_TEMPLATE_JSON_FirstAttribute, '')
        self.firstAttribute = self.convertAttribute(self.firstOriginAttribute)
        self.secondItemId = constaintMap.get(IStatic.IOS_TEMPLATE_JSON_SecondItem, '')
        self.secondOriginAttribute = constaintMap.get(IStatic.IOS_TEMPLATE_JSON_SecondAttribute, '')
        self.secondAttribute = self.convertAttribute(self.secondOriginAttribute)
        self.constant = constaintMap.get(IStatic.IOS_TEMPLATE_JSON_Constant, '')
        self.id = constaintMap.get(IStatic.IOS_TEMPLATE_JSON_Id, '')
        self.priority = constaintMap.get(IStatic.IOS_TEMPLATE_JSON_Priority, '')
        self.symbolic = constaintMap.get(IStatic.IOS_TEMPLATE_JSON_Symbolic, '')

    def convertAttribute(self,attri:str) -> str:
        if IStatic.str_is_empty(attri): return ''
        if attri == _trailing: return _right
        if attri == _leading: return _left
        return attri

    def setupRelation(self):
        if IStatic.str_is_empty(self.relationOrigin):
            self.relation = _str_equalTo
        else:
            self.relation = self.relationOrigin

    def reloadProperty(self):
        self.firstItemName = self.getViewOwnerNameCallback_func(self.firstItemId)
        self.secondItemName = self.getViewOwnerNameCallback_func(self.secondItemId)
        self.constantResultStr = self.makeConstraint()

    def makeConstraint(self) -> str:
        firstName = self.firstItemName
        firstAttribute = self.firstAttribute
        secondName = self.secondItemName
        secondAttribute = self.secondAttribute
        constantOrigin = self.constant
        constantNum:float = 0.0
        constant:str = ''
        if IStatic.str_is_not_empty(constantOrigin) and len(constantOrigin) > 0:
            constantNum = float(constantOrigin)
            if firstAttribute == _right or firstAttribute == _bottom:
                constantNum = -constantNum

        if round(constantNum) == constantNum:
            constant = f'{round(constantNum)}'
        else:
            constant = f'{constantNum}'

        if self.secondItemId == self.viewId and IStatic.str_is_not_empty(self.viewId):
            firstName = self.secondItemName
            firstAttribute = self.secondAttribute
            secondName = self.firstItemName
            secondAttribute = self.firstAttribute

        constantResultStr = _str_make + '.'

        if IStatic.str_is_not_empty(firstAttribute):
            constantResultStr += firstAttribute + '.'

        constantResultStr += self.relation + '('
        if IStatic.str_is_not_empty(secondName) and IStatic.str_is_not_empty(self.secondItemId) and IStatic.str_is_not_empty(self.firstItemId):
            constantResultStr += secondName
            if IStatic.str_is_not_empty(secondAttribute):
                constantResultStr += f'.mas_{secondAttribute})'
            if constantNum != 0:
                constantResultStr += f'.offset({constant})'
        else:
            if constantNum != 0:
                constantResultStr += f'@({constant}))'
            elif (IStatic.str_is_not_empty(secondName) and IStatic.str_is_not_empty(self.secondItemId)):
                constantResultStr += f'{secondName})'
            else:
                constantResultStr += f'@({constant}))'

        if IStatic.str_is_not_empty(self.priority):
            constantResultStr += f'.priority({self.priority})'

        constantResultStr += ';'
        return constantResultStr


class ios_constraints_maker:

    height: str = ''
    width: str = ''
    viewMap: dict = None
    viewId: str = ''
    viewName:str = ''
    constaintResultList:[str] = []
    constaintResultStr: str = ''

    def __init__(self,viewMap:dict):
        self.viewMap = viewMap

    # 定义修饰器
    def getViewOwnerNameCallback(self, func):
        self.getViewOwnerNameCallback_func = func

    def reload_propertys(self):

        self.viewId = self.viewMap.get(IStatic.IOS_TEMPLATE_JSON_NodeId)
        self.viewName = self.getViewOwnerNameCallback_func(self.viewId)
        constaintList = self.viewMap.get(IStatic.IOS_TEMPLATE_JSON_Constraints,{})

        if len(constaintList) == 0:
            return

        constaintResultList = []
        header = f'[{self.viewName} mas_makeConstraints:^(MASConstraintMaker *make) {{'
        constaintResultList.append(header)

        for key, constaintMap in constaintList.items():
            item = ios_constaint_item(constaintMap,self.viewId)
            @item.getViewOwnerNameCallback
            def ios_constaint_item_callback(viewId:str):
                return self.getViewOwnerNameCallback_func(viewId)

            item.reloadProperty()
            constaintResultList.append(item.constantResultStr)

        footer = '}];'
        constaintResultList.append(footer)

        self.constaintResultList = constaintResultList
        self.constaintResultStr = '\n'.join(constaintResultList)

