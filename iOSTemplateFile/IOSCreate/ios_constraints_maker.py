
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
_top = 'top'
_bottom = 'bottom'

class _ios_constraints_item:

    constraints_view:str = ''
    view = ''
    space:str = ''
    self_location:str
    location:str

    def _legal_location(cls,item_enum) -> bool:
        return item_enum == 'left' or item_enum == 'top' or item_enum == 'bottom' or item_enum == 'right'

    def __init__(self,map:dict,view,self_location):
        if isinstance(map,dict) == False:
            return
        self.constraints_view = map.get(Constraints_View)
        self.space = map.get(Constraints_Space,'0')
        self.location = map.get(Constraints_Location,'').lower()
        self.view = view
        self.self_location = self_location

    def make_item_constraint(self):
        consttaint_str = ''

        if isinstance(self.constraints_view,str) and len(self.constraints_view) > 0:
            consttaint_str = f'''make.{self.self_location}.equalTo(self.{self.constraints_view}'''
            if self._legal_location(self.location):
                consttaint_str += f'.mas_{self.location}'
            consttaint_str += ')'
            if isinstance(self.space,str) and len(self.space) > 0:
                consttaint_str += f'.offset({self.space})'

        elif isinstance(self.space,str) and len(self.space) > 0:
            consttaint_str = f'make.{self.self_location}.equalTo(@({self.space}))'
            if  self._legal_location(self.location):
                consttaint_str = f'make.{self.self_location}.equalTo(@(self.{self.view}.superView.mas_{self.location}).offset({self.space})'

        if len(consttaint_str) > 0:
            consttaint_str += ';'
        return consttaint_str

class ios_constraints_maker:
    top: _ios_constraints_item = None
    left: _ios_constraints_item = None
    bottom: _ios_constraints_item = None
    right: _ios_constraints_item = None
    height: str = ''
    width: str = ''
    map: dict = None

    def __init__(self,map):
        self.map = map
        self.reload_propertys(map)

    def reload_propertys(self,map:dict):
        self.view_name = map.get(IStatic.IOS_TEMPLATE_JSON_PropertyNameKey)
        constraint_map: dict = map.get(Constraints_info)

        if isinstance(constraint_map,dict) == False:
            return
        top_map: dict = constraint_map.get(Constraints_Top)
        left_map: dict = constraint_map.get(Constraints_Left)
        bottom_map: dict = constraint_map.get(Constraints_Bottom)
        right_map: dict = constraint_map.get(Constraints_Right)

        self.top = _ios_constraints_item(top_map,self.view_name,_top)
        self.left = _ios_constraints_item(left_map, self.view_name,_left)
        self.bottom = _ios_constraints_item(bottom_map, self.view_name,_bottom)
        self.right = _ios_constraints_item(right_map, self.view_name,_right)
        self.width = constraint_map.get(Constraints_Width)
        self.height = constraint_map.get(Constraints_Height)

    def append_constraints(self,constraint:str,constraint_list:list):
        if len(constraint) == 0:
            return
        constraint_list.append(constraint)

    def makeForMap(self):

        constraintResultList:[str] = []

        constraintList: [str] = []
        #top
        if self.top is not None:
            self.append_constraints(self.top.make_item_constraint(),constraintList)

        #left
        if self.left is not None:
            self.append_constraints(self.left.make_item_constraint(),constraintList)

        #bottom
        if self.bottom is not None:
            self.append_constraints(self.bottom.make_item_constraint(),constraintList)

        #right
        if self.right is not None:
            self.append_constraints(self.right.make_item_constraint(),constraintList)

        if isinstance(self.height,str) and len(self.height) > 0:
            constraintList.append(f'make.height.equalTo(@({self.height}));')

        if isinstance(self.width,str) and len(self.height) > 0:
            constraintList.append(f'make.width.equalTo(@({self.width}));')

        if len(constraintList) > 0:
            constraintResultList.append(f'\n[self.{self.view_name} mas_makeConstraints: ^(MASConstraintMaker * make) {{')
            constraintResultList += constraintList
            constraintResultList.append('}];')

        return '\n'.join(constraintResultList)
