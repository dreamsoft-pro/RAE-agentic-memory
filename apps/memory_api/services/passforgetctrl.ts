javascript
'use strict';

import { ApiService } from '@/lib/api';
import { NotificationService, TranslationService } from '@/services';

angular.module('dpClient.app')
.controller('index.PassForgetCtrl', function($rootScope, $scope, $state, AuthService, UserService) {
    const api = new ApiService();
    const notification = new NotificationService();
    const translation = new TranslationService();

    function init() {
        // [BACKEND_ADVICE] Add initialization logic if necessary
    }

    init();

    $scope.passForget = function() {
        UserService.passForget($scope.email).then((data) => {
            if (data.response) {
                notification.success(translation.translate("new_password_sent"));
                $state.go('login');
            } else {
                notification.error(translation.translate("error"));
            }
        }, () => {
            notification.error(translation.translate("error"));
        });
    };
});
