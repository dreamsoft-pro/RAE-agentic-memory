angular.module('digitalprint.app')
    .controller('shop.DeliveriesCtrl', function ($rootScope, $scope, $q, $filter, $modal, ModuleValueService, DeliveryService,
                                                 ModuleService, TaxService, Notification) {

        $scope.taxes;
        $scope.packageSettings;
        $scope.currLang = $rootScope.currentLang.code;

        TaxService.getAll().then(function (data) {
            $scope.taxes = data;
        });

        DeliveryService.getAll().then(function (data) {
            $scope.deliveries = data;
        });

        ModuleService.getExtended('couriers', 'delivery').then(function (data) {
            $scope.couriers = data;
        });

        ModuleService.getExtended('couriers', 'package').then(function (data) {
            $scope.packageSettings = data;
        });

        ModuleService.getExtended('couriers', 'collection').then(function (data) {
            $scope.collections = data;
        });

        ModuleService.getExtended('couriers', 'collectionAttributes').then(function (data) {
            $scope.collectionAttributes = data;
        });

        $scope.form = {};
        $scope.reset = function () {
            $scope.form = {};
        };

        $scope.refresh = function () {
            DeliveryService.getAll(true).then(function (data) {
                $scope.deliveries = data;
            });
        };

        $scope.selectCourier = function (courierID, form) {
            form.courier = _.findWhere($scope.couriers, {ID: courierID});
            form.courierKeys = {};
        };

        $scope.selectCollection = function (courierID, form) {
            form.collection = _.findWhere($scope.collections, {ID: courierID});
        };

        $scope.add = function () {
            DeliveryService.create($scope.form).then(function (data) {

                $scope.deliveries.push(data);

                $scope.saveModuleSettings(data.ID, $scope.form.courierKeys, $scope.form.courier.key).then(function (data) {
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

        $scope.saveModuleSettings = function (deliveryID, courierKeys, courierKey) {

            var def = $q.defer();

            var module = {
                keys: courierKeys,
                componentID: deliveryID
            };

            if (!_.keys(module.keys).length) {
                def.resolve();
                return def.promise;
            }

            var ValueService = new ModuleValueService(courierKey);

            ValueService.update(module).then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });
            return def.promise;
        };

        $scope.edit = function (delivery) {
            $modal.open({
                templateUrl: 'src/shop/templates/modalboxes/edit-delivery.html',
                scope: $scope,
                resolve: {
                    moduleValues: function () {
                        var courier = _.findWhere($scope.couriers, {ID: delivery.courierID});

                        var ValueService = new ModuleValueService(courier.key);

                        return ValueService.getList({deliveryID: delivery.ID}).then(function (data) {
                            return data;
                        });
                    },
                    collectionAttributes: function() {

                        return ModuleService.getExtended('couriers', 'collectionAttributes').then(function (data) {

                            var collection = _.findWhere(data, {ID: delivery.courierID});

                            return reduceCollectionAttributes(collection).then(function(data) {

                                return data;
                            }, function( dataError ) {
                                return dataError;
                            });
                        });

                    },
                },
                controller: function ($scope, $modalInstance, moduleValues, collectionAttributes) {

                    $scope.delivery = delivery;
                    $scope.form = _.clone(delivery, true);

                    $scope.form.price = delivery.price;

                    if(collectionAttributes) {
                        $scope.collectionAttributes = collectionAttributes.reduced;
                        $scope.form.collectionOption = collectionAttributes.collectionOption;
                    }

                    if ($scope.form.courierID) {
                        $scope.selectCourier($scope.form.courierID, $scope.form);
                        $scope.selectCollection($scope.form.courierID, $scope.form);
                    }

                    for(var courierKey in moduleValues.keys ) {

                        var idx = _.findIndex($scope.form.courier.keys, {ID: parseInt(courierKey)});

                        if( idx > -1 ) {
                            if( typeof $scope.form.courier.keys[idx].value === 'number' ) {
                                $scope.form.courier.keys[idx].value = parseInt(moduleValues.keys[courierKey]);
                            } else {
                                if( typeof moduleValues.keys[courierKey] === 'object' ) {
                                    $scope.form.courier.keys[idx].value = _.values(moduleValues.keys[courierKey])[0];
                                } else {
                                    $scope.form.courier.keys[idx].value = moduleValues.keys[courierKey];
                                }

                            }
                        }
                    }

                    $scope.save = function () {

                        DeliveryService.update($scope.form).then(function (data) {

                            prepareCourierKeys($scope.form.courier).then(function(courierKeys) {

                                $scope.saveModuleSettings(delivery.ID, courierKeys, $scope.form.courier.key).then(function (data) {
                                    $modalInstance.close();
                                    $scope.refresh();
                                    Notification.success($filter('translate')('success'));
                                }, function (data) {
                                    Notification.error($filter('translate')('error'));
                                });
                            }, function (error) {
                                console.info('info: ' + error);
                                $modalInstance.close();
                                Notification.success($filter('translate')('success'));
                            });

                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.addNewOption = function (collectionAttribute) {
                        var index = _.findIndex($scope.collectionAttributes, {ID: collectionAttribute.ID});

                        if( index > -1 ) {
                            $scope.collectionAttributes[index].values.push('');
                        }
                    };

                    $scope.removeOption = function (collectionAttribute, index) {
                        collectionAttribute.values.splice(index, 1);
                        delete $scope.form.collectionOption[collectionAttribute.ID][index];
                    };

                }
            });
        };

        $scope.remove = function (id) {
            DeliveryService.remove(id).then(function (data) {
                var idx = _.findIndex($scope.deliveries, {ID: id});
                if (idx > -1) {
                    $scope.deliveries.splice(idx, 1);
                    Notification.success($filter('translate')('success'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            })
        };

        function reduceCollectionAttributes(collection) {
            var def = $q.defer();

            var reduced = [];
            var collectionOption = {};

            if( collection.keys === undefined ) {
                def.resolve(false);
            }

            _.each(collection.keys, function(row, index) {

                _.each(row.values, function(value, index) {
                    if( collectionOption[row.ID] === undefined ) {
                        collectionOption[row.ID] = {};
                    }
                    collectionOption[row.ID][index] = value;
                });

                if( row.values === undefined ) {
                    row.values = [''];
                }

                reduced.push(row);

                if( (collection.keys.length - 1) === index ) {
                    return def.resolve({
                        'reduced': reduced,
                        'collectionOption': collectionOption
                    });
                }
            });

            return def.promise;
        }

        function prepareCourierKeys(courier) {
            var def = $q.defer();

            var keys = {};

            if( courier.keys === undefined ) {
                def.reject('no keys');
            }

            _.each(courier.keys, function(row, index) {

                keys[row.ID] = row.value;

                if( index === (courier.keys.length - 1) ) {
                    def.resolve(keys);
                }
            });

            return def.promise;
        }


    });
