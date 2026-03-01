angular.module('digitalprint.app')
    .controller('printshop.DepartmentsCtrl', function ($scope, $filter, $modal, DepartmentService, Notification) {

        $scope.sortChange = false;

        $scope.sortableOptions = {
            stop: function(e, ui) {
                $scope.sortChange = true;
            },
            axis: 'y',
            placeholder: 'success',
            handle: 'button.button-sort',
            cancel: ''
        };

        DepartmentService.getAll().then(function (data) {
            $scope.departments = data;
        });

        $scope.add = function () {
            DepartmentService.create($scope.form).then(function (data) {
                $scope.departments.push(data.item);
                $scope.form = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.edit = function (department) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-department.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = department;
                    $scope.department = department;

                    $scope.ok = function () {

                        DepartmentService.update($scope.form).then(function (data) {
                            if( data.response ) {
                                department = data.item;
                                $modalInstance.close();
                                Notification.success($filter('translate')('success'));
                            } else {
                                Notification.error($filter('translate')('error'));
                            }
                        });
                    }
                }
            });
        };

        $scope.remove = function (id) {
            DepartmentService.remove(id).then(function (data) {
                if( data.response ) {
                    var idx = _.findIndex($scope.departments, {ID: id});
                    if( idx > -1 ) {
                        $scope.departments.splice(idx, 1);
                    }
                    Notification.success($filter('translate')('success'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            })
        };

        $scope.sortCancel = function () {
            $scope.refresh();
            $scope.sortChange = false;
        };

        $scope.sortSave = function () {
            var result = [];
            _.each($scope.departments, function (item) {
                result.push(item.ID);
            });

            DepartmentService.sort(result).then(function (data) {
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