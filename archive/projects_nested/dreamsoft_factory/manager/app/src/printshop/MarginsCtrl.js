angular.module('digitalprint.app')
    .controller('printshop.MarginsCtrl', function ($scope, $filter, $modal, DeviceService, Notification,
                                                   PsPricelistService, PsConfigAttributeNatureService, MarginsService) {

        $scope.marginForm = {};
        $scope.supplierMarginForm = {};
        PsPricelistService.getAll().then(function (data) {
            $scope.priceList = data;
        }, function (error) {
            console.error(error)
        });

        PsConfigAttributeNatureService.getAll().then(function (data) {
            $scope.natures = data;
        });

        MarginsService.getAllSuppliers().then(function (data) {
            $scope.suppliers = data;
        });

        function loadMargins() {
            if (!$scope.selectedPriceListID || !$scope.selectedNatureID) {
                return;
            }
            MarginsService.get($scope.selectedPriceListID, $scope.selectedNatureID).then(function (data) {
                $scope.margins = data;
            });
        }

        function loadSupplierMargins() {
            MarginsService.getSupplierMargins().then(function (data) {
                $scope.supplierMargins = data;
            });
        }

        loadSupplierMargins();

        $scope.onPriceClick = function (priceListID) {
            $scope.selectedPriceListID = priceListID;
            loadMargins()
        }

        $scope.onNatureClick = function (natureID) {
            $scope.selectedNatureID = natureID;
            loadMargins()
        }

        $scope.addMargin = function () {
            var data = _.clone($scope.marginForm);
            data.priceTypeID = $scope.selectedPriceListID;
            data.natureID = $scope.selectedNatureID;
            MarginsService.add(data).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('success'));
                    $scope.marginForm = {};
                    loadMargins()
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function (error) {
                Notification.error($filter('translate')('error'));
            })
        }

        $scope.editMarginBegin = function (margin) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-margin.html',
                controller: function ($scope, $modalInstance) {
                    $scope.marginForm = _.clone(margin);
                    $scope.save = function () {
                        MarginsService.edit(margin.ID, $scope.marginForm).then(function (data) {
                            if (data.response) {
                                Notification.success($filter('translate')('success'));
                                $modalInstance.close();
                                loadMargins();
                            } else {
                                Notification.error($filter('translate')('error'));
                            }

                        }, function (error) {
                            Notification.error($filter('translate')('error'));
                        });

                    }

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })
        }

        $scope.removeMargin = function (marginID) {
            MarginsService.removeMargin(marginID).then(function (data) {
                    if (data.response) {
                        Notification.success($filter('translate')('success'));
                        loadMargins()
                    } else {
                        Notification.error($filter('translate')('error'));
                    }
                },
                function (error) {
                    Notification.error($filter('translate')('error'));
                })
        }

        $scope.addSupplierMargin = function () {
            MarginsService.addSupplierMargins($scope.supplierMarginForm).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('success'));
                    $scope.supplierMarginForm = {};
                    loadSupplierMargins()
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function (error) {
                Notification.error($filter('translate')('error'));
            })
        }

        $scope.editSupplierMargin = function (margin) {
            $modal.open({
                scope: $scope,
                templateUrl: 'src/printshop/templates/modalboxes/edit-supplier-margin.html',
                controller: function ($scope, $modalInstance) {
                    $scope.supplierMarginForm = _.clone(margin);
                    $scope.save = function () {
                        MarginsService.editSupplierMargins(margin.ID, $scope.supplierMarginForm).then(function (data) {
                            if (data.response) {
                                Notification.success($filter('translate')('success'));
                                $modalInstance.close();
                                loadSupplierMargins();
                            } else {
                                Notification.error($filter('translate')('error'));
                            }

                        }, function (error) {
                            Notification.error($filter('translate')('error'));
                        });

                    }

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })
        }

        $scope.removeSupplierMargin = function (marginID) {
            MarginsService.removeSupplierMargin(marginID).then(function (data) {
                    if (data.response) {
                        Notification.success($filter('translate')('success'));
                        loadSupplierMargins();
                    } else {
                        Notification.error($filter('translate')('error'));
                    }
                },
                function (error) {
                    Notification.error($filter('translate')('error'));
                })
        }
    });
