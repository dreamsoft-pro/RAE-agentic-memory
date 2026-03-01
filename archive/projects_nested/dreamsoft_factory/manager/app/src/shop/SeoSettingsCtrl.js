/**
 * Created by Rafał on 23-08-2017.
 */
angular.module('digitalprint.app')
    .controller('shop.SeoSettingsCtrl', function ($scope, $filter, Notification, SettingService) {

        var settings = new SettingService('seoSettings');
        $scope.currentData = {};

        $scope.invoiceVatStatuses = [];

        $scope.form = {
            gaIdCode: {
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
            settings.setModule('seoSettings');
            $scope.form.domainID = $scope.currentDomain.ID;
            console.log($scope.form);
            settings.save($scope.form).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        function init() {

        }

        init();

    });