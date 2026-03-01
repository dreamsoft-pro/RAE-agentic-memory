angular.module('digitalprint.app')
    .controller('printshop.MarginsTypeCtrl', function ($scope, $filter, $modal, $stateParams, DeviceService, Notification,
                                                   PsPricelistService, PsConfigAttributeNatureService, MarginsService) {
        var currentGroupID =  $stateParams.groupID;
        var currentTypeID =  $stateParams.typeID;
        $scope.marginForm = {};
        PsPricelistService.getAll().then(function (data) {
            $scope.priceList = data;
        }, function (error) {
            console.error(error)
        });

        PsConfigAttributeNatureService.getAll().then(function (data) {
            $scope.natures = data;
        });


        function loadMargins() {
            if (!$scope.selectedPriceListID || !$scope.selectedNatureID) {
                return;
            }
            MarginsService.get($scope.selectedPriceListID, $scope.selectedNatureID, '', currentTypeID).then(function (data) {
                $scope.margins = data;
            });
        }

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
            data.typeID = currentTypeID;
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

    });
