angular.module('digitalprint.app')
    .controller('shop.ConfigMailCtrl', function ($scope, $filter, $rootScope, SettingService, Notification) {

        var settings = new SettingService('mail');

        $scope.form = {
            ssl: {
                value: ''
            },
            from: {
                value: ''
            },
            fromName: {
                _type: 'textarea'
            },
            host: {
                value: ''
            },
            passwd: {
                value: ''
            },
            port: {
                value: ''
            },
            username: {
                _type: 'text',
                value: ''
            }
        };

        settings.getAll().then(function (data) {
            $scope.currentData = _.merge($scope.form, data);
            $scope.reset();
        });

        $scope.reset = function () {
            $scope.form = _.clone($scope.currentData, true);
        };

        $scope.save = function () {
            settings.setModule('mail');
            settings.save($scope.form).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

    });