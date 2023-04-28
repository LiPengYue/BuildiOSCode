
#import "iOSTemplateViewModel.h"
#import "iOSTemplateTableViewCell.h"

@interface iOSTemplateViewModel()

@end

@implementation iOSTemplateViewModel

- (CGFloat)getContainerViewHeight {
    return [iOSTemplateTableViewCell getContainerViewHeightWithViewModel:self];
}
@end
