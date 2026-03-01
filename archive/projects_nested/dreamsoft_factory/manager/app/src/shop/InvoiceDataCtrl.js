/**
 * Created by Rafał on 14-07-2017.
 */
angular.module('digitalprint.app')
    .controller('shop.InvoiceDataCtrl', function ($scope, $filter, Notification, SettingService) {

        var settings = new SettingService('invoiceData');

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
            location: {
                value: ''
            },
            nip: {
                value: ''
            },
            bankAccount: {
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

        $scope.saveInvoiceData = function () {
            settings.setModule('invoiceData');
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