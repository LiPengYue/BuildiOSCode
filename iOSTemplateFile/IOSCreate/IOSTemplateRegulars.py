import re

def IOS_TEMPLATE_REGULAR(regular): return '\/\/<#Regular: {regular} #>'.format(regular=regular)
def Regular_StartPropertyKey(): return IOS_TEMPLATE_REGULAR('propertys')
def Regular_StartSetUpPropertyKey(): return IOS_TEMPLATE_REGULAR('setUpPropertyValue')
def Regular_GeeterAndSetterKey(): return IOS_TEMPLATE_REGULAR('getter&&setter')
def Regular_ConstraintsKey(): return IOS_TEMPLATE_REGULAR('constraintsSubview')


def getRegularStringAToStringB(strA:str,strB:str):
    return f'(?<={strA}).*?(?={strB})'

def isNotEmptyStr(str):
    return len(str) == 0 or str == None

def getStrAToStrB(strA:str,strB:str,contentStr:str):
    if isNotEmptyStr(strA) or isNotEmptyStr(strB):
        return contentStr
    result = re.findall(getRegularStringAToStringB(strA,strB),contentStr,flags=re.DOTALL)
    return result

def insert_str(regular,insert,content_str) -> str:
    r = re.search(regular, content_str, flags=re.DOTALL)
    if r is None:
        print(f'\n{r}🌶未匹配到')
        return content_str
    location = r.end()
    front = content_str[:location]
    last = content_str[location:]
    content_str = front + insert + last
    return content_str

def remove_regular_str(regular,content_str) -> str:
    r = re.search(regular, content_str, flags=re.DOTALL)
    if r is None:
        print(f'\n{r}🌶未匹配到')
        return content_str
    location = r.end()
    front = content_str[:r.start()]
    last = content_str[r.end():]
    content_str = front + last
    return content_str
