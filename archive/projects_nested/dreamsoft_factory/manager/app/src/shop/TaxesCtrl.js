angular.module('digitalprint.app')
    .controller('shop.TaxesCtrl', function ($scope, $filter, $modal, TaxService, Notification) {

        TaxService.getAll().then(function (data) {
            $scope.taxes = data;
        });

        $scope.reset = function () {
            $scope.form = {};
        };

        $scope.refresh = function () {
            TaxService.getAll(true).then(function (data) {
                $scope.taxes = data;
            });
        };

        $scope.add = function () {
            TaxService.create($scope.form).then(function (data) {
                $scope.taxes.push(data);
                $scope.reset();
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.edit = function (tax) {
            $modal.open({
                templateUrl: 'src/shop/templates/modalboxes/edit-tax.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = $scope.tax = _.clone(tax);

                    $scope.ok = function () {
                        $scope.form.active = parseInt($scope.form.active);
                        TaxService.update($scope.form).then(function (data) {
                            if ($scope.form['default'] === 1) {
                                _.each($scope.taxes, function (item) {
                                    item['default'] = 0;
                                })
                            }
                            tax = _.extend(tax, $scope.form);
                            $scope.form = {};
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        });
                    }
                }
            });
        };

        $scope.remove = function (id) {
            TaxService.remove(id).then(function (data) {
                var idx = _.findIndex($scope.taxes, {ID: id});
                if (idx > -1) {
                    $scope.taxes.splice(idx, 1);
                    Notification.success($filter('translate')('success'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            })
        };


    });