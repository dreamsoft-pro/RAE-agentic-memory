/**
 * Created by Rafał on 16-03-2017.
 */
angular.module('digitalprint.app')
    .controller('contents.LayoutSettingsCtrl', function ($scope, $filter, $rootScope, SettingService, Notification) {

        $scope.skins = [];
        $scope.menuTypes = [1, 2];
        $scope.websiteStyles = [
            {'value': 1, name: 'standard'},
            {'value': 2, name: 'style_for_website'}
        ];
        var settings = new SettingService('skins');

        $scope.form = {
            menuLeft: {
                value: 0
            },
            skinName: {
                value: ''
            },
            webMasterVerifyTag: {
                value: ''
            },
            numberOfVolumesInOffer: {
                value: ''
            },
            numberOfLinesInDescription: {
                value: ''
            },
            menuType: {
                value: 1
            },
            websiteStyle: {
                value: 1
            }
        };

        settings.getAll().then(function (data) {
            $scope.skins = data;

            settings.setModule('general');

            settings.getAll().then(function (data) {
                $scope.currentData = _.merge($scope.form, data);
                $scope.reset();
            });
        });

        $scope.reset = function () {
            $scope.form = _.clone($scope.currentData, true);
        };

        $scope.save = function () {
            settings.save($scope.form).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

    });