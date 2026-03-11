javascript
'use strict';

const api = require('@/lib/api');

function initController($scope, DpAddressService, CountriesService) {
    $scope.countries = [];

    function init() {
        getDefaultAddress();
    }

    // [BACKEND_ADVICE] Fetch default address and populate form.
    function getDefaultAddress() {
        return DpAddressService.getDefaultAddress(2).then(data => {
            $scope.form = data.address;
            return CountriesService.getAll().then(dataCountries => {
                $scope.countries = dataCountries;
            });
        });
    }

    init();
}

function editInvoice($scope) {
    $scope.form.type = 2;
    $scope.form.default = 1;
}

angular.module('dpClient.app')
    .controller('client-zone.InvoiceDataCtrl', function ($scope, $rootScope, DpAddressService, CountriesService,
                                                         Notification, $filter) {
        initController($scope, DpAddressService, CountriesService);
        $scope.edit = editInvoice.bind(null, $scope);
    });
