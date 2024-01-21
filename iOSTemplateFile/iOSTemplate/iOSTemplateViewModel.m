
#import "iOSTemplateViewModel.h"
#import "iOSTemplateBaseView.h"

@interface iOSTemplateViewModel()

@end

@implementation iOSTemplateViewModel

- (CGFloat)getContainerViewHeight {
    return [iOSTemplateBaseView getContainerViewHeightWithViewModel:self];
}
@end
