//
//  UIView+PYBaseBuildCodeXIB.h
//  XIB
//
//  Created by 李鹏跃 on 2023/1/31.
//

#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

@interface UIView (PYBaseBuildCodeXIB)
///倒角
@property (nonatomic, assign) IBInspectable   CGFloat  cornerRadius;
///边框颜色
@property (nonatomic, strong) IBInspectable   UIColor *borderColor;
///边框宽度
@property (nonatomic, assign) IBInspectable   CGFloat  borderWidth;
@property (nonatomic, copy) IBInspectable NSString *propertyName;
@property (nonatomic, copy) IBInspectable NSString *bgColorAPI;
 
@end

NS_ASSUME_NONNULL_END
