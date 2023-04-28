def special(name) -> str:
    if 'parameter' in name:
        return f'\n@property (nonatomic,copy) NSDictionary *{name};'
    return None
