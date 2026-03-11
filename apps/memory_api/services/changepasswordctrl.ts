javascript
'use strict';

angular.module('dpClient.app')
.controller('client-zone.ChangePasswordCtrl', function ($scope, Notification, $filter, UserService) {

    // Initialize controller
    function init() {
        // [BACKEND_ADVICE] Consider initializing form fields here if necessary.
    }

    init();

    // Change password functionality
    $scope.change = function () {
        
        if( $scope.form.pass !== $scope.form.confirmPass ) {
            Notification.error($filter('translate')('passwords_not_same'));
            return;
        }

        UserService.changePass($scope.form).then(handleSuccess, handleError);

        function handleSuccess(data) {
            if(data.response === true) {
                Notification.success($filter('translate')('successfully_edited'));
            } else {
                Notification.error($filter('translate')('error'));
            }
        }

        function handleError() {
            Notification.error($filter('translate')('error'));
        }
    };
});
