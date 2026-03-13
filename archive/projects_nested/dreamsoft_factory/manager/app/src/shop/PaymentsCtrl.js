angular.module('digitalprint.app')
    .controller('shop.PaymentsCtrl', function ($scope, $q, $filter, $modal, ModuleValueService,
                                               ModuleService, PaymentService, Notification, UserService) {

        $scope.sellers = [];

        PaymentService.getAll().then(function (data) {
            $scope.payments = data;
        });

        PaymentService.getAll().then(function (data) {
            $scope.paymentTypes = data;
        });

        ModuleService.getExtended('payment').then(function (data) {
            $scope.paymentSettings = data;
        });

        UserService.getUsersByType().then( function(data) {
            $scope.sellers = data;
        });

        $scope.selectPayment = function (mainComponentID, form) {
            form.payment = _.findWhere($scope.paymentSettings, {ID: mainComponentID});
            form.paymentKeys = {};
        };

        $scope.form = {};
        $scope.reset = function () {
            $scope.form = {};
        };

        $scope.refresh = function () {
            PaymentService.getAll(true).then(function (data) {
                $scope.payments = data;
            });
        };


        $scope.add = function () {

            $scope.form.componentID = $scope.form.mainComponentID;

            PaymentService.create($scope.form).then(function (data) {
                if (data.ID > 0) {
                    $scope.payments.push(data);
                }

                $scope.form.componentID = data.ID;

                $scope.saveModuleSettings(data.ID, $scope.form.paymentKeys).then(function (data) {
                    Notification.success($filter('translate')('success'));
                    $scope.refresh();
                    $scope.form = {};
                }, function (data) {
                    Notification.error($filter('translate')('error'));
                });

            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.saveModuleSettings = function (componentID, paymentkeys) {
            var def = $q.defer();

            var module = {
                keys: paymentKeys,
                componentID: componentID
            };

            var ValueService = new ModuleValueService(data.payment.key);

            ValueService.update(module).then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });
            return def.promise;
        };

        $scope.edit = function (payment) {

            var _payment = payment;

            $modal.open({
                templateUrl: 'src/shop/templates/modalboxes/edit-payment.html',
                scope: $scope,
                resolve: {
                    moduleValues: function () {

                        var paymentModule = _.findWhere($scope.paymentSettings, {ID: _payment.componentID});

                        var ValueService = new ModuleValueService(paymentModule.key);

                        return ValueService.getList({componentID: _payment.ID}).then(function (data) {
                            return data;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, moduleValues) {
                    $scope.payment = payment;
                    $scope.form = _.clone(_payment, true);

                    $scope.form.mainComponentID = _payment.componentID;

                    if ($scope.form.mainComponentID) {
                        $scope.selectPayment($scope.form.mainComponentID, $scope.form);
                    }

                    $scope.form.paymentKeys = moduleValues.keys;

                    $scope.save = function () {
                        PaymentService.update($scope.form).then(function (data) {
                            if (data.response === true) {
                                payment = _.extend(payment, $scope.form);
                            }

                            preparePaymentKeys($scope.form).then(function (paymentKeys) {

                                $scope.saveModuleSettings(payment.ID, paymentKeys).then(function (data) {
                                    $modalInstance.close();
                                    $scope.refresh();
                                    $scope.form = {};
                                    Notification.success($filter('translate')('success'));
                                }, function (data) {
                                    Notification.error($filter('translate')('error'));
                                });

                            }, function () {
                                $modalInstance.close();
                                Notification.success($filter('translate')('success'));
                            });


                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.remove = function (id) {
            PaymentService.remove(id).then(function (data) {
                var idx = _.findIndex($scope.payments, {ID: id});
                if (idx > -1) {
                    $scope.payments.splice(idx, 1);
                    Notification.success($filter('translate')('success'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            })
        }

        function preparePaymentKeys(payment) {
            var def = $q.defer();

            var keys = {};

            if( payment.paymentKeys === undefined ) {
                def.reject('no keys');
            }

            _.each(payment.paymentKeys, function(row, index) {

                keys[row.ID] = row.value;

                if( index === (payment.paymentKeys.length - 1) ) {
                    def.resolve(keys);
                }
            });

            return def.promise;
        }


    });