//
//  Root
//  template_projectNameKey
//  Created by template_userNameKey on 2022/12/10.
//  Copyright © 2022 template_userNameKey. All rights reserved.
//  


#import <UIKit/UIKit.h>

@class
ZRRentRootModel,
ZRRentRootListModel,
ZRRentRootListImageConfigModel,
ZRRentRootListTitlesModel;

@protocol
ZRRentRootListModel,
ZRRentRootListTitlesModel;

@interface ZRRentRootModel : NSObject
@property (nonatomic,copy) NSArray<ZRRentRootListModel> *list;
@end

@protocol ZRRentRootListModel<NSObject> @end
@interface ZRRentRootListModel : NSObject
@property (nonatomic,copy) NSArray<NSString *> *icon;
@property (nonatomic,strong) ZRRentRootListImageConfigModel *imageConfig;
@property (nonatomic,copy) NSArray<ZRRentRootListTitlesModel> *titles;
@end

@interface ZRRentRootListImageConfigModel : NSObject
@property (nonatomic,copy) NSString *img;
@property (nonatomic,assign) NSInteger size;
@end

@protocol ZRRentRootListTitlesModel<NSObject> @end
@interface ZRRentRootListTitlesModel : NSObject
@property (nonatomic,copy) NSString *subTitle;
@property (nonatomic,copy) NSString *title;
@end
