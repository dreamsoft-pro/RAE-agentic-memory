angular.module('digitalprint.app')
    .controller('shop.CurrenciesCtrl', function ($scope, $filter, $modal, CurrencyRootService, CurrencyService, Notification) {

        CurrencyRootService.getAll().then(function (data) {
            $scope.currenciesRoot = data;
        });

        CurrencyService.getAll().then(function (data) {
            $scope.currencies = data;
        });

        $scope.reset = function () {
            $scope.form = {};
        };

        $scope.refresh = function () {
            CurrencyService.getAll(true).then(function (data) {
                $scope.currencies = data;
            });
        };

        $scope.add = function () {
            CurrencyService.create($scope.form).then(function (data) {
                var currency = _.findWhere($scope.currenciesRoot, {code: data.code});
                data.name = currency.name;
                $scope.currencies.push(data);
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.edit = function (currency) {
            $modal.open({
                templateUrl: 'src/shop/templates/modalboxes/edit-currency.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = $scope.currency = _.clone(currency);

                    $scope.ok = function () {
                        CurrencyService.update($scope.form).then(function (data) {
                            if ($scope.form['default'] === 1) {
                                _.each($scope.currencies, function (item) {
                                    item['default'] = 0;
                                })
                            }
                            currency = _.extend(currency, $scope.form);
                            $scope.form = {};
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        });
                    }
                }
            });
        };

        $scope.remove = function (id) {
            CurrencyService.remove(id).then(function (data) {
                var idx = _.findIndex($scope.currencies, {ID: id});
                if (idx > -1) {
                    $scope.currencies.splice(idx, 1);
                    Notification.success($filter('translate')('success'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            })
        }

    });