# 导入模块
from iOSTemplateFile.IOSCreate import ios_static_string as IStatic

def is_suffix_bracket_left(line):
    line_temp = line.lstrip()
    last = IStatic.IOS_TEMPLATE_char_bracket_left + IStatic.IOS_TEMPLATE_char_newline
    return len(line_temp) >= 2 and last in line_temp

def is_prefix_bracket_right(line):
    line_temp = line.lstrip()
    return len(line_temp) >= 1 and IStatic.IOS_TEMPLATE_char_bracket_right in line_temp

def indent(line,layer:int=0):
    if len(line.lstrip()) == 0:
        return line
    if layer < 0:
        layer = 0
    return IStatic.IOS_TEMPLATE_char_tab * layer + line.lstrip()

def format(path:str):
    result_lines: [str] = []
    result_str = ''
    with open(path, "r") as f:
        # all = f.read()
        f.seek(0, 0) #如果之前有red，需要把光标移动到开头，否则 f.readlines()为空
        layer:int = 0
        lines = f.readlines()
        for line in lines:
            if is_prefix_bracket_right(line):
                layer = layer - 1

            line = indent(line, layer)
            result_lines.append(line)
            result_str += line

            if is_suffix_bracket_left(line):
                layer += 1

    if len(result_lines) != len(lines):
        return
    with open(path,'w+') as f:
        f.write(result_str)