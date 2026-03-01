/**
 * Created by Rafał on 20-07-2017.
 */
angular.module('digitalprint.app')
    .controller('shop.SenderDataCtrl', function ($scope, $filter, Notification, SettingService, CountriesService) {

        var settings = new SettingService('senderData');

        $scope.countries = [];

        $scope.form = {
            companyName: {
                value: ''
            },
            street: {
                value: ''
            },
            houseNumber: {
                value: ''
            },
            flatNumber: {
                value: ''
            },
            postalCode: {
                value: ''
            },
            city: {
                value: ''
            },
            country: {
                value: ''
            },
            contactPerson: {
                value: ''
            },
            phone: {
                value: ''
            },
            email: {
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

        $scope.saveSenderData = function () {
            settings.setModule('senderData');
            settings.save($scope.form).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        function init() {
            CountriesService.getAllEnabled().then(function(countries) {
                $scope.countries = countries;
            });
        }

        init();

    });