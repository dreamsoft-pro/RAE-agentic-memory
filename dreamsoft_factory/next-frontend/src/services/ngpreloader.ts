javascript
import { apiUrl } from '@/lib/api';

const directiveNgPreLoader = ($config, $rootScope) => ({
    restrict: 'A',
    template: '<div class="pre-loader" ng-show="preloaderOn">' +
              '<img loading="lazy" src="{{loader}}">' +
              '</div>',
    scope: {
        preloaderOn: '='
    },
    link: function (scope) {
        if ($rootScope.companyID) {
            // [BACKEND_ADVICE] Consider fetching the loader path from backend service instead of constructing it manually.
            scope.loader = apiUrl($config.STATIC_URL + '/' + $rootScope.companyID + '/images/pre-loader.gif');
        } else {
            scope.loader = '';
        }
    }
});

export default directiveNgPreLoader;
