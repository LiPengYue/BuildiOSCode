### Python根据Json生成Objective-c代码



为了学习Python3.9，我构思了一个Python生成Objective-c代码项目，以项目来推动学习，让学习更有动力，学习成果更加扎实。



## 目标：

1、  解析UI稿（HTML文件），根据HTML生成完整的Objective-c代码（未完成）

- 完成了xcode XIB 解析成json，json转Objective-c代码

2、 根据json生成ViewModel、model、View文件，（完成）

3、 根据json自动给模板添加 子视图、视图布局、视图属性赋值的代码（完成）



## Json 数据源获取：

### 一、 UI稿转json（未完成）

终极目标是把蓝湖HTML文件转成一个个可解析的json，然后转成Objective-c代码，但是前端代码不是很熟悉，所以先用xcode的xib进行了json转化



### 二、 Xcode XIB 转json

#### XIB 可视化编辑属性

每个子UI视图，生成代码都需要有几个要素：

1、视图样式相关： border、borderColor，backgroundColor，text，image等

2、 网络接口相关：image， text， backgroundColor等

为了在XIB中展示这些接口，方便为json生成提供数据，我在OC demo中添加了几个分类（添加IBInspectable标识，表示可以在xib中展示）



```objective-c
// View
@interface UIView (PYBaseBuildCodeXIB)
@property (nonatomic, assign) IBInspectable   CGFloat  cornerRadius;//圆角
@property (nonatomic, strong) IBInspectable   UIColor *borderColor;//边框颜色
@property (nonatomic, assign) IBInspectable   CGFloat  borderWidth;//边框宽度
@property (nonatomic, copy) IBInspectable NSString *propertyName;
@property (nonatomic, copy) IBInspectable NSString *bgColorAPI;
@end
  
// label
@interface UILabel (PYBaseBuildCodeXIB)
@property (nonatomic, copy) IBInspectable NSString *textColorAPI;
@property (nonatomic, copy) IBInspectable NSString *textAPI;
@end

// image
@interface UIButton (PYBaseBuildCodeXIB)
@property (nonatomic, copy) IBInspectable NSString *textColorAPI;
@property (nonatomic, copy) IBInspectable NSString *textAPI;
@end

// image
@interface UIImageView (PYBaseBuildCodeXIB)
@property (nonatomic, copy) IBInspectable NSString *imageAPI;
@end
```

![截屏2024-01-21 下午3.19.37](https://p.ipic.vip/uiltw8.png)



#### XIB 解析

HTML解析：XIB会生成一个HTML文件，解析HTML使用的是`xml.dom.minidom`三方库，

常量字符存储：HTML中特定的标签字段由`iOSXIBDomParserStaticStr.py`来存储

解析model：

有基类iOSXIBDomParserButtonModel来处理View的一些基本属性记录，比如 borderColor、布局相关数据等

子类记录特有的属性值

<img src="https://p.ipic.vip/dmt17x.png" alt="截屏2024-01-21 下午3.48.56" style="zoom:50%;" />

#### 使用

iOSXIBDomParser ,构造函数传入xib绝对路径，调用viewModel.convertToDic函数来解析成字典

```python
parser = iOSXIBDomParser(path)
contentDict = parser.viewModel.convertToDic()
```



##  Json 生成Objective-c代码

### 代码生成的思路步骤

![image2022-12-25_18-18-8](https://p.ipic.vip/jz0v90.png)



1、 解析Json，获取json中的属性定义列表、赋值子视图网络数据列表、懒加载视图属性列表、布局数据列表

> 时机开发中，我们经常使用宏定义来创建UIColor、UIFont，所以工具提供了colorConfig.txt、fontConfig.txt文件来配置创建规则
>
> ```json
> colorConfig.txt
>  {
>      "annotation_NetApiCreateColor": "根据字段创建UIColor对象,'#colorName#' 为字段名",
>      "NetApiCreateColor":"[UIColor : colorWithName: #colorName#]",
>      "annotation_DefineHexCreateColor": "根据宏定义创建UIColor对象,'#colorName#' 为16进制参数",
>      "DefineHexCreateColor":"ColorDefine(#colorName#)",
>      "annotation_StaticCreateColorList": "默认宏定义UIColor对象数组,key为宏定义，value为16进制颜色",
>      "DefineCreateColorList": [
>          "define_red":"0xFFFF0000"
>      ]
>  }
> 
> fontConfig.txt
> {
>         "annotation_DefineCreateFont": "根据字体名创建UIFont对象,'#FontSize#' 会替换成float类型",
>         "DefineCreateFont": {
> 
>             "PingFangSC-Regular": "FontPingFangSCR(#fontSize#)",
>             "PingFangSC-Medium": "FontPingFangSCM(#fontSize#)",
>             "PingFangSC-Light": "FontPingFangSCL(#fontSize#)",
>         },
>         "annotation_CreateFont": "根据family_name创建UIFont对象,'#familyName#' 为font名, #fontSize#为size",
>         "CreateFont": "[UIFont fontWithName:#familyName# size:#fontSize#]",
> }
> ```



2、 根据模板文件，把对应的数据生成代码，插入到模板代码对应的位置中

> 在模板代码中，插入对应的关键字，使用正则来匹配对应的位置，具体代码参见：IOSTemplateRegulars.py

3、 格式化代码格式：ios_code_style.py

4、 输出view/viewModel文件

> 在输出文件的时候，需要标注文件头信息以及存储的位置，提供了rootConfig.text来进行配置
>
> ```json
> {
>          "template_userNameKey": "名称",
>          "template_nickNameKey": "昵称",
> 
>          "baseViewModelName": "viewModel的父类",
>          "dataSouceName": "view持有的ViewModel属性名",
> 
>          "templateViewName": "模板View名",
>          "templateBaseViewName": "模板view父类名",
>          "templateViewLayoutPointerName":"模板view承载子视图的view属性名",
> 
>          "templateViewModelName": "模板ViewModel名",
>          "templateBaseViewModelName": "模板ViewModel父类名",
> 
>          "templateViewPath": "模板view的路径",
>          "templateViewModelPath": "模板ViewModel路径",
> 
>          "savePath": "生成的代码存储路径"
> 
>      }
> ```
>
> 生成之后的头文件目录为



### 代码生成工具的代码结构

![截屏2024-01-21 下午4.50.51](/Users/lp1/Library/Application Support/typora-user-images/截屏2024-01-21 下午4.50.51.png)

### 使用：

步骤：

1、 创建一个Objective-c项目，把目录中的`PYBaseBuildCodeXIB`  与 `iOSTemplate`文件夹拖入项目中

2、 创建xib文件，并布局视图、 xib文件右边填写各个子视图的参数：api、propertyName...

3、 找到ios_code_builder.py文件运行man函数

4、 配置弹出的colorConfig.text、 fontConfig.text、rootConfig.text文件

5、 在控制台回车，后完成代码转化

事例：

![image-20240121171809004](https://p.ipic.vip/razoro.png)



![image-20240121172403305](https://p.ipic.vip/5wlzsz.png)

生成的cell.m文件

```objective-c
//
//  PYXIBViewCell
//  生成View
//  Created by 李鹏跃 on 2024/1/21.
//  Copyright © 2024 lpy. All rights reserved.
//  


#import "PYXIBViewCell.h"

@interface PYXIBViewCell()

@property (nonatomic,strong) UILabel *titleLabel;
@property (nonatomic,strong) UILabel *subTitle;
@property (nonatomic,strong) UIImageView *coverImage;
@property (nonatomic,strong) UIButton *byButton;

@end

@implementation PYXIBViewCell
- (instancetype)initWithStyle:(UITableViewCellStyle)style reuseIdentifier:(NSString *)reuseIdentifier {
    if (self = [super initWithStyle:style reuseIdentifier:reuseIdentifier]) {
        [self setupViews];
    }
    return self;
}

- (void)didSetBaseViewModel:(iOSTemplateTableBaseViewModel *)baseViewModel {
    if (![baseViewModel isKindOfClass:PYXIBViewCellViewModel.class]) {
        return;
    }
    self.viewModel = (PYXIBViewCellViewModel *)baseViewModel;
}

- (void) setViewModel:(PYXIBViewCellViewModel *)viewModel {
    _viewModel = viewModel;
    
    // titleLabel
    self.titleLabel.text = self.viewModel.title;
    self.titleLabel.textColor = [UIColor py_colorWithHex: self.viewModel.titleColor ?: @"0xFAFAFA"];
                  
    // subTitle
    self.subTitle.text = self.viewModel.subTitle;
    self.subTitle.textColor = [UIColor py_colorWithHex: self.viewModel.subTitleColor ?: @"0xFAFAFA"];
                  
    // coverImage
    [self.coverImage sd_setImageWithURL:[NSURL URLWithString:self.viewModel.cover?:@""]];

}

- (void)setupViews {
    
    [self.contentView addSubview:self.titleLabel];
    [self.contentView addSubview:self.subTitle];
    [self.contentView addSubview:self.coverImage];
    [self.contentView addSubview:self.byButton];

    [self.titleLabel mas_makeConstraints:^(MASConstraintMaker *make) {
        make.height.equalTo(@(17));
        make.top.equalTo(self.coverImage.mas_top);
        make.left.equalTo(self.coverImage.mas_right).offset(8);
        make.right.lessThanOrEqualTo(@(-16));
    }];
    [self.subTitle mas_makeConstraints:^(MASConstraintMaker *make) {
        make.height.equalTo(@(14));
        make.top.equalTo(self.titleLabel.mas_bottom).offset(8);
        make.left.equalTo(self.titleLabel.mas_left);
    }];
    [self.coverImage mas_makeConstraints:^(MASConstraintMaker *make) {
        make.width.equalTo(@(60));
        make.height.equalTo(@(60));
        make.top.equalTo(self.contentView.mas_top).offset(10);
        make.left.equalTo(self.contentView.mas_left).offset(16);
    }];
    [self.byButton mas_makeConstraints:^(MASConstraintMaker *make) {
        make.height.equalTo(@(44));
        make.width.equalTo(@(44));
        make.right.equalTo(@(-16));
        make.bottom.equalTo(self.contentView);
    }];
}

// MARK: - getter && setter

- (UILabel *) titleLabel {
    if (!_titleLabel) {
        _titleLabel = [[UILabel alloc]init];
        _titleLabel.layer.borderColor = KColorRGB(0xFFFF00FF).CGColor;
        _titleLabel.layer.borderWidth = 1;
        _titleLabel.layer.cornerRadius = 2;
        _titleLabel.textColor = KColorRGB(0xFF222222);
        _titleLabel.font = KFontR(12);
        _titleLabel.textAlignment = NSTextAlignmentLeft;
        _titleLabel.text = @"titleLabel";
    }
    return _titleLabel;
}

- (UILabel *) subTitle {
    if (!_subTitle) {
        _subTitle = [[UILabel alloc]init];
        _subTitle.textColor = KColorRGB(0x8032ADE6);
        _subTitle.font = KFontR(10);
        _subTitle.textAlignment = NSTextAlignmentLeft;
        _subTitle.text = @"subTitle";
    }
    return _subTitle;
}

- (UIImageView *) coverImage {
    if (!_coverImage) {
        _coverImage = [[UIImageView alloc]init];
        _coverImage.layer.cornerRadius = 4;
    }
    return _coverImage;
}
- (UIButton *) byButton {
    if (!_byButton) {
        _byButton = [[UIButton alloc]init];
        _byButton.layer.borderColor = KColorRGB(0xFFEB0159).CGColor;
        _byButton.layer.borderWidth = 1;
        _byButton.layer.cornerRadius = 2;
        [_byButton setTitleColor:KColorRGB(0xFFEB0159) forState:UIControlStateNormal];
        _byButton.titleLabel.font = KFontR(12);
        [self.byButton setTitle:@"购买" forState: UIControlStateNormal];
        [_byButton addTarget:self action:@selector(click_byButton) forControlEvents:UIControlEventTouchUpInside];
    }
    return _byButton;
}
- (void)click_byButton {
        
}

// MARK: - containerHeight
+ (CGFloat)getContainerViewHeightWithViewModel:(iOSTemplateTableBaseViewModel *)viewModel {
    if (![viewModel isKindOfClass:PYXIBViewCellViewModel.class]) {
        return CGFLOAT_MIN;
    }
    PYXIBViewCellViewModel *vm = (PYXIBViewCellViewModel *)viewModel;
    CGFloat h = CGFLOAT_MIN;
    return h;
}


@end

```

viewModel.h文件

```objective-c
//
//  PYXIBViewCellViewModel
//  生成View
//  Created by 李鹏跃 on 2024/1/21.
//  Copyright © 2024 lpy. All rights reserved.
//  


#import "iOSTemplateBaseViewModel.h"

NS_ASSUME_NONNULL_BEGIN

@interface PYXIBViewCellViewModel : iOSTemplateBaseViewModel
@property (nonatomic,copy) NSString *titleColor;
@property (nonatomic,copy) NSString *title;
@property (nonatomic,copy) NSString *subTitleColor;
@property (nonatomic,copy) NSString *subTitle;
@property (nonatomic,copy) NSString *cover;

@end

NS_ASSUME_NONNULL_END

```

