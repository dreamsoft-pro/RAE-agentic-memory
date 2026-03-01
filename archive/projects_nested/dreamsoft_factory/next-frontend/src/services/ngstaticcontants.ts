javascript
import { ApiService } from '@/lib/api';

export const ngStaticContentsDirective = (StaticContentService, $rootScope, $interpolate) => ({
    restrict: 'A',
    template: '<div ta-bind ng-model="contentObject.contents[currentLangCode]"></div>',
    scope: {
        content: '@'
    },
    link: function(scope, elem, attrs) {
        scope.contentObject = {};

        StaticContentService.getContent(scope.content).then(data => {
            scope.contentObject.contents = {};
            
            if ($rootScope.currentLang) {
                const currentLangCode = $rootScope.currentLang.code;
                scope.contentObject.contents[currentLangCode] = '';
            }
        });
    }
});

// [BACKEND_ADVICE] Consider moving heavy logic related to content retrieval and language handling to backend services for better separation of concerns.

angular.module('dpClient.helpers').directive('ngStaticContents', ngStaticContentsDirective);
