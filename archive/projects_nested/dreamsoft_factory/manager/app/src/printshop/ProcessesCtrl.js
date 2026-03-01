angular.module('digitalprint.app')
    .controller('printshop.ProcessesCtrl', function ($scope, $modal, $filter, Notification, ProcessService) {

        ProcessService.getAll().then(function (data) {
            $scope.processes = data;
        }, function (data) {
            console.log("Error", data);
        });

        $scope.sortChange = false;
        $scope.sortableOptions = {
            stop: function (e, ui) {
                $scope.sortChange = true;
            },
            axis: 'y',
            placeholder: 'success',
            handle: 'button.button-sort',
            cancel: ''
        };

        $scope.refresh = function () {
            ProcessService.getAll(true).then(function (data) {
                $scope.processes = data;
            });
        };

        $scope.add = function () {
            ProcessService.create($scope.form).then(function (data) {
                $scope.processes.push(data);
                $scope.form = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.edit = function (process) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-process.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.process = _.clone(process);
                    $scope.form = _.clone(process);

                    $scope.ok = function () {
                        ProcessService.update($scope.form).then(function (data) {
                            process = _.extend(process, $scope.form);
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        });
                    }
                }
            });
        };

        $scope.remove = function (id) {
            ProcessService.remove(id).then(function (data) {
                var idx = _.findIndex($scope.processes, {ID: id});
                $scope.processes.splice(idx, 1);
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error') + " " + data.info)
            })
        };

        $scope.sortCancel = function () {
            $scope.refresh();
            $scope.sortChange = false;
        };

        $scope.sortSave = function () {
            var result = [];
            _.each($scope.processes, function (item) {
                result.push(item.ID);
            });

            ProcessService.sort(result).then(function (data) {
                $scope.sortChange = false;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
                $scope.sortCancel();
            });
        };

        $scope.search = function () {
            var newFilter = {};
            for(var filter in $scope.filterData){
                if($scope.filterData[filter] != ''){
                    newFilter[filter] = $scope.filterData[filter];
                }
            }
            $scope.filterData = newFilter;
        };

    });