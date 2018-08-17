
#import <UIKit/UIKit.h>

typedef NS_ENUM(NSInteger, NMVideoType) {
  NMVideoTypeA = 1,
  NMVideoTypeB = 2,
};

@protocol NMVideoDetailViewControllerInParamsBuilder <NSObject>
@property (nonatomic, copy) id<NMVideoDetailViewControllerInParamsBuilder>(^mvId)(NSString *mvId);
@property (nonatomic, copy) id<NMVideoDetailViewControllerInParamsBuilder>(^type)(NMVideoType type);
@end

@protocol NMVideoDetailViewControllerOutParams <NSObject>
@property (nonatomic, assign) BOOL canceled;
@end

@protocol NMUserDetailViewControllerInParamsBuilder <NSObject>
@property (nonatomic, copy) id<NMUserDetailViewControllerInParamsBuilder>(^mvId)(NSString *mvId);
@end

@protocol NMUserDetailViewControllerOutParams <NSObject>
@property (nonatomic, assign) BOOL canceled;
@end

@interface Navigator (NMVideoModule)
- (void)openVideoDetailWithParams:(void(^)(id<NMVideoDetailViewControllerInParamsBuilder> builder))builder finish:(void(^)(id<NMVideoDetailViewControllerOutParams> result, NSError *error))finish;
- (void)openUserDetailWithParams:(void(^)(id<NMUserDetailViewControllerInParamsBuilder> builder))builder finish:(void(^)(id<NMUserDetailViewControllerOutParams> result, NSError *error))finish;
@end

