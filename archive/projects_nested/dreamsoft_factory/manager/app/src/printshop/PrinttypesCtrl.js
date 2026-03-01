angular.module('digitalprint.app')
    .controller('printshop.PrinttypesCtrl', function ($scope, $rootScope, $filter, $q, Notification, PsWorkspaceService, PsPricelistService, PsPrintTypeService, DeviceService, $modal) {

        function init() {

            PsPrintTypeService.getAll().then(function (data) {
                $scope.printtypes = data;
            });

            $q.all([
                PsWorkspaceService.getAll(),
                PsPricelistService.getAll()
            ]).then(function (data) {
                $scope.workspaces = data[0];
                $scope.priceLists = data[1];
                $scope.resetForm();
            });

            $rootScope.$on('ps_workspaces', function (e, data) {
                $scope.workspaces = data;
            });
            $rootScope.$on('ps_priceLists', function (e, data) {
                $scope.priceLists = data;
            });

        }

        $scope.resetForm = function () {
            $scope.form = {};
            $scope.form.pricelistID = $scope.priceLists[0].ID;
            $scope.form.workspaceID = $scope.workspaces[0].ID;
        };

        $scope.refresh = function () {
            PsPrintTypeService.getAll(true).then(function (data) {
                $scope.printtypes = data;
            });
        };

        $scope.getWorkspace = function (workspaceID) {
            return _.find($scope.workspaces, {ID: workspaceID});
        };

        $scope.getPricelist = function (printtype) {
            return _.find($scope.priceLists, {ID: printtype.pricelistID});
        };

        $scope.add = function () {
            PsPrintTypeService.add($scope.form).then(function (data) {
                $scope.resetForm();
                $scope.printtypes.push(data);
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.edit = function (item) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-printtype.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.oryg = item;
                    $scope.form = angular.copy(item);

                    $scope.save = function () {
                        $scope.form.workspaceID = null;
                        PsPrintTypeService.edit($scope.form).then(function (data) {
                            var idx = _.findIndex($scope.printtypes, {ID: item.ID});
                            if (idx > -1) {
                                $scope.printtypes[idx] = angular.copy($scope.form);
                            }
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }
                }
            })
        };

        $scope.devices = function (printtype) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/devices-selector.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.selectorTitle = $filter('translate')('print_type') + ' ' + printtype.name;
                    $scope.printtype = _.clone(printtype);
                    $scope.currentDevices = [];
                    DeviceService.getAll().then(function (data) {
                        $scope.currentDevices = _.clone(data, true);
                        PsPrintTypeService.devices(printtype).then(function (data) {
                            _.each(data, function (item) {
                                var idx = _.findIndex($scope.currentDevices, {ID: item});
                                if (idx > -1) {
                                    $scope.currentDevices[idx].selected = 1;
                                }
                            })
                        })
                    });

                    $scope.ok = function () {
                        var selectedDevices = [];
                        _.each($scope.currentDevices, function (each) {
                            if (each.selected === 1) {
                                selectedDevices.push(each.ID);
                            }
                        });

                        PsPrintTypeService.setDevices(printtype, selectedDevices).then(function (data) {
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.remove = function (item) {
            PsPrintTypeService.remove(item).then(function (data) {
                var idx = _.findIndex($scope.printtypes, {ID: item.ID});
                if (idx > -1) {
                    $scope.printtypes.splice(idx, 1);
                    Notification.success($filter('translate')('success'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        init();

    });
