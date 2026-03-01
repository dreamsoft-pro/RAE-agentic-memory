angular.module('digitalprint.app')
    .controller('printshop.WorkspacesCtrl', function ($scope, $filter, Notification, PsWorkspaceService, $modal,
                                                      $rootScope, DeviceService) {

        function init() {
            $scope.types = [
                {
                    ID: 1,
                    name: $filter('translate')('standard')
                },
                {
                    ID: 2,
                    name: $filter('translate')('roller')
                },
                {
                    ID: 3,
                    name: $filter('translate')('unlimited')
                }
            ];


            $scope.resetForm();

            getWorkspaces();

        }

        $scope.resetForm = function () {
            $scope.form = {};
            $scope.form.type = $scope.types[0].ID;
        }

        $scope.refresh = function () {
            PsWorkspaceService.getAll(true).then(function (data) {
                $scope.workspaces = data;
            });
        }

        var getWorkspaces = function () {
            PsWorkspaceService.getAll().then(function (data) {
                $scope.workspaces = data;
                //wszytaj templatke
            }, function (data) {
                //nara
            });
        }

        $scope.getWorkspaceType = function (workspace) {
            return _.find($scope.types, {ID: workspace.type});
        }

        $scope.add = function () {
            PsWorkspaceService.add($scope.form).then(function (data) {
                $scope.resetForm();
                $scope.workspaces = data;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

        $scope.edit = function (item) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-workspace.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.oryg = item;
                    $scope.form = angular.copy(item);

                    $scope.save = function () {
                        PsWorkspaceService.edit($scope.form).then(function (data) {
                            getWorkspaces();
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    }

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }
                }
            })
        };

        $scope.devices = function (workspace) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/devices-selector.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.selectorTitle = $filter('translate')('workspace') + ' ' + workspace.name;
                    $scope.currentDevices = [];
                    DeviceService.getAll().then(function (data) {
                        $scope.currentDevices = _.clone(data, true);
                        PsWorkspaceService.devices(workspace).then(function (data) {
                            _.each(data, function (item) {
                                var idx = _.findIndex($scope.currentDevices, {ID: item.deviceID});
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

                        PsWorkspaceService.setDevices(workspace, selectedDevices).then(function (data) {
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
            PsWorkspaceService.remove(item).then(function (data) {
                $scope.workspaces = data;
                Notification.success($filter('translate')('success'));

            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };


        init();

    });
