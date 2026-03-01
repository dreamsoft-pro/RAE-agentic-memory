javascript
import { createDirective } from '@/lib/api';

export const ngConfirmClickDirective = createDirective({
    name: 'ngConfirmClick',
    directive: function () {
        return {
            restrict: 'A',
            replace: false,
            link: (scope, element, attr) => {
                const clickAction = attr.ngConfirmClick;

                // [BACKEND_ADVICE] Heavy logic should be moved to backend if needed.
                element.bind('click', event => {
                    scope.open();

                    scope.onConfirm = () => {
                        scope.$eval(clickAction);
                    };
                });
            },
            controller: function ($scope, $rootScope, $filter, $modal, $sce, $attrs, $config) {
                const clickAction = $attrs.ngConfirmClick;

                // [BACKEND_ADVICE] Ensure that the logic here is optimized and lean.
            }
        };
    }()
});
