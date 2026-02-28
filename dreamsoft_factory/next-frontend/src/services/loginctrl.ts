javascript
// Used in unauthorized and base view
import { BackendApi } from '@/lib/api';
import { UserService, AuthService, DomainService, DpAddressService, Notification, LoginWidgetService, SocialWidgetService, MainWidgetService } from './services';

export default class IndexLoginCtrl {
    constructor($rootScope, $scope, $state, $filter, $window, $http) {
        this.$rootScope = $rootScope;
        this.$scope = $scope;
        this.$state = $state;
        this.$filter = $filter;
        this.$window = $window;
        this.$http = $http;

        // [BACKEND_ADVICE] MainWidgetService.includeTemplateVariables is heavy logic
        MainWidgetService.includeTemplateVariables($scope, 'login');
        
        if (!_.isUndefined($state.current.data)) {
            $rootScope.bodyClass = $state.current.data.bodyClass;
        }

        $rootScope.rememberLogin = false;

        new BackendApi().init();
    }
}

IndexLoginCtrl.$inject = ['$rootScope', '$scope', '$state', '$filter', '$window', '$http'];
