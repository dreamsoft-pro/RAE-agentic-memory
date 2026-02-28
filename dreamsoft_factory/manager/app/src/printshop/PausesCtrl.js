angular.module('digitalprint.app')
    .controller('printshop.PausesCtrl', function($scope, $filter, $modal, PauseService, Notification) {

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

        PauseService.getAll().then(function(data) {
            $scope.pauses = data;
        });

        $scope.add = function() {
            PauseService.create($scope.form).then(function(data) {
                $scope.pauses.push(data.item);
                $scope.form = {};
                Notification.success($filter('translate')('success'));
            }, function(data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.edit = function(pause) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-department.html',
                scope: $scope,
                controller: function($scope, $modalInstance) {
                    $scope.form = pause;
                    $scope.pause = pause;

                    $scope.ok = function() {

                        PauseService.update($scope.form).then(function(data) {
                            if (data.response) {
                                pause = data.item;
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

        $scope.remove = function(id) {
            PauseService.remove(id).then(function(data) {
                if (data.response) {
                    var idx = _.findIndex($scope.pauses, { ID: id });
                    if (idx > -1) {
                        $scope.pauses.splice(idx, 1);
                    }
                    Notification.success($filter('translate')('success'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function(data) {
                Notification.error($filter('translate')('error'));
            })
        };

        $scope.sortCancel = function() {
            $scope.refresh();
            $scope.sortChange = false;
        };

        $scope.sortSave = function() {
            var result = [];
            _.each($scope.pauses, function(item) {
                result.push(item.ID);
            });

            PauseService.sort(result).then(function(data) {
                $scope.sortChange = false;
                Notification.success($filter('translate')('success'));
            }, function(data) {
                Notification.error($filter('translate')('error'));
                $scope.sortCancel();
            });
        };

        $scope.savePauses = function() {

            if( this.pauses ) {

                PauseService.updateReportSheets(this.pauses).then( function(saved) {
                    if( saved.response ) {
                        Notification.success($filter('translate')('success'));
                    } else {
                        Notification.error($filter('translate')('error'));
                    }
                }, function(saved) {
                    Notification.error($filter('translate')('error'));
                });

            }

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