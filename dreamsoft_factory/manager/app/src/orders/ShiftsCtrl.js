angular.module('digitalprint.app')
    .controller('orders.ShiftsCtrl', function ($scope, $filter, $modal, ShiftService, Notification) {

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

        ShiftService.getAll().then(function (data) {
            $scope.shifts = data;
        });

        $scope.add = function () {
            ShiftService.create($scope.form).then(function (data) {
                $scope.shifts.push(data.item);
                $scope.form = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.edit = function (shift) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/edit-shift.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = shift;
                    $scope.shift = shift;

                    $scope.ok = function () {

                        ShiftService.update($scope.form).then(function (data) {
                            if( data.response ) {
                                shift = data.item;
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
            ShiftService.remove(id).then(function (data) {
                if( data.response ) {
                    var idx = _.findIndex($scope.shifts, {ID: id});
                    if( idx > -1 ) {
                        $scope.shifts.splice(idx, 1);
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
            _.each($scope.shifts, function (item) {
                result.push(item.ID);
            });

            ShiftService.sort(result).then(function (data) {
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