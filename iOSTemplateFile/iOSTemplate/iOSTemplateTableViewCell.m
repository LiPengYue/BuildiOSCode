

#import "iOSTemplateTableViewCell.h"

@interface iOSTemplateTableViewCell()
//<#Regular: propertys #>
@end

@implementation iOSTemplateTableViewCell
- (instancetype)initWithStyle:(UITableViewCellStyle)style reuseIdentifier:(NSString *)reuseIdentifier {
    if (self = [super initWithStyle:style reuseIdentifier:reuseIdentifier]) {
        [self setupViews];
    }
    return self;
}

- (void)didSetBaseViewModel:(iOSTemplateTableBaseViewModel *)baseViewModel {
    if (![baseViewModel isKindOfClass:iOSTemplateViewModel.class]) {
        return;
    }
    self.viewModel = (iOSTemplateViewModel *)baseViewModel;
}

- (void) setViewModel:(iOSTemplateViewModel *)viewModel {
    _viewModel = viewModel;
    //<#Regular: setUpPropertyValue #>
}

- (void)setupViews {
    //<#Regular: constraintsSubview #>
}

// MARK: - getter && setter
//<#Regular: getter&&setter #>

// MARK: - containerHeight
+ (CGFloat)getContainerViewHeightWithViewModel:(iOSTemplateTableBaseViewModel *)viewModel {
    if (![viewModel isKindOfClass:iOSTemplateViewModel.class]) {
        return CGFLOAT_MIN;
    }
    iOSTemplateViewModel *vm = (iOSTemplateViewModel *)viewModel;
    CGFloat h = CGFLOAT_MIN;
    return h;
}


@end
