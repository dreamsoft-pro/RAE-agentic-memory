javascript
import { api } from '@/lib/api';

angular.module('dpClient.helpers')
    .directive('ngInitBind', function($compile) {
        return {
            restrict: 'A',
            link: function(scope, element, attr) {
                // [BACKEND_ADVICE] Evaluate the condition and compilation logic here.
                attr.$observe('ngBindHtml', function() {
                    if (attr.ngBindHtml) {
                        $compile(element[0].children)(scope);
                    }
                });
            }
        };
    });
