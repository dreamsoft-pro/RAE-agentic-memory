angular.module('digitalprint.app')
    .controller('shop.SupportedCountriesCtrl', function ($rootScope, $scope, $filter, $modal, CurrencyRootService, CountriesService, Notification) {

        $scope.countries = [];
        $scope.currLang = $rootScope.currentLang.code;
        $scope.saveData = false;
        $scope.isDefaultChecked = false;

        $scope.$watch(function() {
            return $rootScope.currentLang;
          }, function() {
            $scope.currLang = $rootScope.currentLang.code;
          }, true);


        CountriesService.getAll().then(function (data) {
            $scope.countries = data;
            data.forEach(function (country) {
                if (country.isDefault)
                    $scope.isDefaultChecked = true;
            });
        });

        $scope.refresh = function () {
            $scope.saveData = false;
            $scope.isDefaultChecked = false;
            CountriesService.getAll(true).then(function (data) {
                $scope.countries = data;
                data.forEach(function (country) {
                    if (country.isDefault)
                        $scope.isDefaultChecked = true;
                });
            });
        };

        $scope.search = function () {
            var newFilter = {};
            for (var filter in $scope.filterData) {
                if ($scope.filterData[filter] != '') {
                    newFilter[filter] = $scope.filterData[filter];
                }
            }
            if ($scope.filterName !== '') {
                newFilter['name_' + $scope.currLang] = $scope.filterName;
            }else{
                delete newFilter['name_' + $scope.currLang];
            }

            $scope.filterData = newFilter;
        };

        $scope.checker = function () {
            $scope.saveData = true;
        };

        $scope.setDefault = function (country) {
            if (country.isDefault) {
                if ($scope.isDefaultChecked) {
                    Notification.error($filter('translate')('default_country_already_checked'));
                    country.isDefault = !country.isDefault;
                } else {
                    $scope.saveData = true;
                    $scope.isDefaultChecked = true;
                }
            } else {
                $scope.isDefaultChecked = false;
            }
            $scope.saveData = true;
        };

        $scope.cancel = function () {
            $scope.refresh();
        };

        $scope.save = function () {
            CountriesService.updateDisabled($scope.countries).then(function (data) {
                $scope.refresh();
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.checkAllCountries = function () {
            $scope.saveData = true;
            $scope.countries.forEach(function (country) {
                country.disabled = false;
            });
        };

        $scope.unCheckAllCountries = function () {
            $scope.saveData = true;
            $scope.countries.forEach(function (country) {
                country.disabled = true;
            });
        };

    });