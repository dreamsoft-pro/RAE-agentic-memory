javascript
import { BackendAdvice, ApiService } from '@/lib/api';

const directiveModule = angular.module('dpClient.helpers');

directiveModule.directive('langConditional', function($compile, $filter) {
    return {
        restrict: 'A',
        link: (scope, element, attrs) => {
            const translation = $filter('translate')(attrs['langConditional']);
            
            // [BACKEND_ADVICE] Heavy logic should be offloaded to the backend for lean design.
            if (!translation || translation === attrs['langConditional']) {
                element.replaceWith('');
            } else if (element[0].childNodes.length === 1 && element[0].childNodes[0].nodeType === 3) {
                element.text(translation);
            }
        }
    };
});
