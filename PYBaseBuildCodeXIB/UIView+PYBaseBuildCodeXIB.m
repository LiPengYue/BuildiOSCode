//
//  UIView+PYBaseBuildCodeXIB.m
//  XIB
//
//  Created by 李鹏跃 on 2023/1/31.
//

#import "UIView+PYBaseBuildCodeXIB.h"

@implementation UIView (PYBaseBuildCodeXIB)

/**
 *  设置边框宽度
 *
 *  @param borderWidth 可视化视图传入的值
 */
- (void)setBorderWidth:(CGFloat)borderWidth {
 
    if (borderWidth < 0) return;
 
    self.layer.borderWidth = borderWidth;
}
 
/**
 *  设置边框颜色
 *
 *  @param borderColor 可视化视图传入的值
 */
- (void)setBorderColor:(UIColor *)borderColor {
 
    self.layer.borderColor = borderColor.CGColor;
}
 
/**
 *  设置圆角
 *
 *  @param cornerRadius 可视化视图传入的值
 */
- (void)setCornerRadius:(CGFloat)cornerRadius {
 
    self.layer.cornerRadius = cornerRadius;
    self.layer.masksToBounds = cornerRadius > 0;
}

@end
