'use strict';

angular.module('digitalprint.app')
    .controller('printshop.ComplexProductsCtrl', function ($q, $rootScope, $scope, $stateParams, $filter, Notification, $modal, PsComplexService, PsGroupService, PsTypeService, getData, PsFormatService) {
        var currentGroupID;
        var currentTypeID;

        $scope.formats = [];
        currentGroupID = $scope.currentGroupID = $stateParams.groupID;
        currentTypeID = $scope.currentTypeID = $stateParams.typeID;
        $scope.form = {};

        $rootScope.currentTypeName = getData.type.name;
        $rootScope.currentGroupName = getData.group.name;

        $scope.currentProduct = false;
        $scope.currentType = false;

        var ComplexService = new PsComplexService(currentGroupID, currentTypeID);

        function getComplex() {
            var def = $q.defer();
            ComplexService.getAll().then(function (data) {
                $scope.complexGroups = data;
                def.resolve(data);
            }, function (data) {
                def.reject(data);
                Notification.error($filter('translate')('data_retrieve_failed'));
            });
            return def.promise;
        }

        getComplex();

        PsGroupService.getAll().then(function (data) {
            $scope.products = data;
        }, function (data) {
            Notification.error($filter('translate')('error'));
        });

        $scope.selectProduct = function (product) {
            $scope.types = false;
            $scope.currentProduct = product;
            PsTypeService.getAll($scope.currentProduct.ID).then(function (data) {
                $scope.types = data;
            }, function (data) {
                $scope.currentProduct = false;
                Notification.error($filter('translate')('data_retrieve_failed'));
            });
        };

        $scope.selectType = function (type) {
            $scope.currentComplexGroups = [];
            _.each($scope.complexGroups, function (item) {
                if (item.type == 'other') {
                    return true;
                }
                $scope.currentComplexGroups.push({ID: item.ID, name: item.name});
            });

            console.log($scope.currentComplexGroups.length);
            if ($scope.currentComplexGroups.length < 1) {
                addProduct(currentTypeID, type, null);
                return true;
            }
            $scope.currentComplexGroups.unshift({ID: null, name: $filter('translate')('no_group')});

            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/complex-product-select-group.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.save = function () {
                        addProduct(currentTypeID, type, $scope.form.complexGroupID).then(function (data) {
                            $modalInstance.close();
                        });
                    };
                }
            });
        };

        $scope.goToProducts = function () {
            $scope.currentProduct = false;
            $scope.currentType = false;
        };

        function addProduct(baseID, type, complexGroupID) {
            var def = $q.defer();

            ComplexService.add(baseID, type.ID, complexGroupID).then(function (data) {
                def.resolve(data);
                $scope.currentProduct = false;
                $scope.currentType = false;
                getComplex().then(function (data) {
                    Notification.success($filter('translate')('success'));
                });
            }, function (data) {
                def.reject(data);
                $scope.currentProduct = false;
                $scope.currentType = false;
                Notification.error($filter('translate')('error'));
            });
            return def.promise;
        }

        $scope.remove = function (group, product) {
            ComplexService.remove(product.ID).then(function (data) {
                getComplex().then(function (data) {
                    Notification.success($filter('translate')('success'));
                });
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.addGroup = function (product) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/add-complex-group.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {

                    $scope.save = function () {
                        ComplexService.addGroup(product.ID, $scope.form.name).then(function (data) {
                            getComplex().then(function (data) {
                                $modalInstance.close();
                            });

                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.editGroup = function (group) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-complex-group.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.group = _.clone(group, true);
                    $scope.form.name = $scope.group.name;
                    $scope.save = function () {
                        ComplexService.editGroup(group.ID, $scope.form.name).then(function (data) {
                            getComplex().then(function (data) {
                                $modalInstance.close();
                            });

                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.relatedFormats = function (product) {
            console.log(product);
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/complex-product-related-formats.html',
                scope: $scope,
                size: 'lg',
                resolve: {
                    formats: function ($q) {
                        var def = $q.defer();
                        var FormatService = new PsFormatService(product.groupID, product.typeID);
                        FormatService.getAll().then(function (data) {
                            def.resolve(data);
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                            def.reject(data);
                        });
                        return def.promise;
                    }
                },
                controller: function ($scope, $modalInstance, formats) {
                    $scope.formats = formats;
                    $scope.currentFormatID = null;
                    $scope.product = _.clone(product, true);
                    $scope.changeFormat = false;

                    $scope.getFormats = function () {
                        $scope.changeFormat = false;
                        if ($scope.currentFormatID === null) {
                            return false;
                        }
                        $scope.selectedFormats = [];
                        ComplexService.relatedFormat($scope.currentFormatID, product.complexID).then(function (data) {
                            $scope.selectedFormats = [];
                            _.each(data, function (item) {
                                $scope.selectedFormats.push(item.formatID);
                            });

                            _.each($scope.complexGroups, function (group, idx) {
                                if (idx === 0) {
                                    return true;
                                }
                                _.each(group.products, function (each) {
                                    var FormatService = new PsFormatService(each.groupID, each.typeID);
                                    FormatService.getAll().then(function (data) {
                                        each.formats = _.clone(data, true);
                                        _.each(each.formats, function (format) {
                                            var idx = $scope.selectedFormats.indexOf(format.ID);
                                            if (idx > -1) {
                                                format.selected = true;
                                            }
                                        });
                                    });
                                });
                            });
                        }, function (data) {
                            $scope.currentFormatID = null;
                            Notification.error($filter('translate')('error'));
                        });

                    };

                    $scope.selectFormat = function (format) {
                        $scope.changeFormat = true;
                        format.selected = !format.selected;
                    };

                    $scope.save = function () {
                        var result = [];
                        _.each($scope.complexGroups, function (group, idx) {
                            if (idx === 0) {
                                return true;
                            }
                            _.each(group.products, function (each) {
                                _.each(each.formats, function (format) {
                                    if (format.selected) {
                                        result.push({typeID: each.typeID, formatID: format.ID});
                                    }
                                });
                            });
                        });

                        ComplexService.saveRelatedFormat($scope.currentFormatID, result, product.complexID)
                            .then(function (data) {
                                $scope.changeFormat = false;
                                Notification.success($filter('translate')('success'));
                            }, function (data) {
                                Notification.error($filter('translate')('error'));
                            });
                        return true;
                    };
                }
            });
        }

    });