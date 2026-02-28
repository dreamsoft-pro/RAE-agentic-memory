javascript
import { createDirective } from '@/lib/api';

export default createDirective('ngAction', () => ({
    restrict: 'A',
    scope: {
        ngAction: '='
    },
    link: function(scope, el, attrs) {
        scope.$watch('ngAction', (action) => {
            el[0].action = action;
        });
    }
}));
