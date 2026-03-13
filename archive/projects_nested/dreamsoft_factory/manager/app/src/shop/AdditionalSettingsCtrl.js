/**
 * Created by Rafał on 23-08-2017.
 */
angular.module('digitalprint.app')
    .controller('shop.AdditionalSettingsCtrl', function ($scope, $filter, Notification, SettingService) {

        var settings = new SettingService('additionalSettings');
        $scope.currentData = {};

        $scope.invoiceVatStatuses = [];

        $scope.form = {
            onlyForCompanies: {
                value: ''
            },
            reclamationDays: {
                value: ''
            },
            rssFeed: {
                value: ''
            },
            captchaPrivateKey: {
                value: ''
            },
            captchaPublicKey: {
                value: ''
            },
            'adminMailRecipients': {
                value: ''
            },
            rssCharLimit: {
                value: ''
            },
            confirmButtonInCart: {
                value: ''
            },
            confirmTextInCart: {
                _type: 'textarea'
            },
            recalculateInCart: {
                value: ''
            },
            separateConfirmButton: {
                value: ''
            },
            calcWithoutDelivery: {
                value: ''
            },
            wcgaUsed: {
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
            settings.setModule('additionalSettings');
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
