angular.module('digitalprint.app')
    .controller('superadmin.CreateCompanyCtrl', function ($scope, ConfigService, Notification, $filter) {

        $scope.form = {};

        $scope.saveCompany = function () {
            console.log($scope.form);
            ConfigService.createCompany($scope.form).then(function (data) {
                $scope.form = {};
                Notification.success($filter('translate')('saved_message'));
            }, function (data) {
                console.log(data);
                Notification.error($filter('translate')('error'));
            });

        }

    });