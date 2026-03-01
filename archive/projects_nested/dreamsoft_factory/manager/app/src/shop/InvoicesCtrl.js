/**
 * Created by Rafał on 14-07-2017.
 */
angular.module('digitalprint.app')
    .controller('shop.InvoicesCtrl', function ($scope, $filter, Notification, DpStatusService, SettingService) {

        var settings = new SettingService('invoice');

        $scope.invoiceVatStatuses = [];

        $scope.numerationData = [
            {value: '', name: 'select'},
            {value: 1, name: 'monthly'},
            {value: 2, name: 'annually'}
        ];

        $scope.form = {
            invoiceOn: {
                value: ''
            },
            invoiceText: {
                _type: 'textarea'
            },
            proformaInvoiceMask: {
                value: ''
            },
            invoiceMask: {
                value: ''
            },
            invoiceVatStatuses: {
                value: '',
                _type: 'text'
            },
            numerationInvoices: {
                value: ''
            }
        };

        settings.getAll().then(function (data) {
            if( data.invoiceVatStatuses && typeof data.invoiceVatStatuses.value === 'string') {
                $scope.invoiceVatStatuses = data.invoiceVatStatuses.value.split(',').map(Number);
            } else {
                $scope.invoiceVatStatuses.push(data.invoiceVatStatuses.value);
            }
            $scope.currentData = _.merge($scope.form, data);
            $scope.reset();
        });

        $scope.reset = function () {
            $scope.form = _.clone($scope.currentData, true);
        };

        $scope.saveInvoice = function () {
            $scope.form.invoiceVatStatuses.value = $scope.invoiceVatStatuses.join(',');
            settings.setModule('invoice');
            settings.save($scope.form).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        function init() {
            DpStatusService.getAll(1).then(function (data) {
                $scope.statuses = data;
            });
        }

        init();

    });