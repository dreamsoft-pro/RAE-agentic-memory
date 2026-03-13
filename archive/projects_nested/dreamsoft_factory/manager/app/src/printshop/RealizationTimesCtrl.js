angular.module('digitalprint.app')
    .controller('printshop.RealizationTimesCtrl', function (SettingService, $q, $translate, $scope, $filter,
                                                            RealizationTimeService, Notification, $modal,
                                                            PsWorkingHourService) {

        var settings = new SettingService('realizationTime');

        $scope.weekDays = [
            1,2,3,4,5,6,7
        ];

        $scope.workingHoursForm = {};

        function init() {


            $scope.settingsForm = {
                hourType: {
                    value: ''
                },
                hour: {
                    value: ''
                },
                workingSaturday: {
                    value: ''
                },
                workingSunday: {
                    value: ''
                },
                domainID: 0
            };


            $scope.hourTypes = [
                {
                    value: 1,
                    name: 'tmpName'
                },
                {
                    value: 2,
                    name: 'tmpName'
                }
            ];

            $scope.realisationColors = {
                0: '#45b6af',
                1: '#E26A6A',
                2: '#ffe567'
            };

            $translate('rt_start').then(function (rt_start) {
                $scope.hourTypes[0].name = rt_start;
            });
            $translate('rt_end').then(function (rt_end) {
                $scope.hourTypes[1].name = rt_end;
            });

            $scope.form = {};
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

            RealizationTimeService.getAll().then(function (data) {
                _.each(data, function (one, index) {
                    if (one.color === null || one.color === '') {
                        one.color = $scope.realisationColors[index % 3];
                    }
                });
                $scope.realizationTimes = data;
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

            settings.getAll().then(function (data) {
                $scope.currentData = _.merge($scope.settingsForm, data);
            });

            PsWorkingHourService.getAll().then(function(data) {
                $scope.workingHoursForm = data;
            });
        }

        init();

        $scope.saveSettings = function () {
            console.log($scope.settingsForm);
            settings.save($scope.settingsForm).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.resetSettings = function () {
            $scope.settingsForm = _.clone($scope.currentData, true);
        };

        $scope.refreshTimes = function () {
            RealizationTimeService.getAll(true).then(function (data) {
                $scope.sortChange = false;
                $scope.realizationTimes = data;
            });
        };

        $scope.add = function () {

            console.log($scope.form);

            RealizationTimeService.add($scope.form).then(function (data) {
                $scope.realizationTimes.push(data);
                $scope.form = {};
                Notification.success($filter('translate')('success') + " " + data.name);
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });


        };

        $scope.editStart = function (elem) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-realizationtime.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.oryg = elem;
                    $scope.form = angular.copy(elem);

                    $scope.save = function () {

                        RealizationTimeService.edit($scope.form).then(function (data) {
                            var idx = _.findIndex($scope.realizationTimes, {ID: $scope.oryg.ID});
                            if (idx > -1) {
                                $scope.realizationTimes[idx] = angular.copy($scope.form);
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

        $scope.sortCancel = function () {
            $scope.refreshTimes();
        };

        $scope.sortSave = function () {
            var result = [];
            _.each($scope.realizationTimes, function (elem) {
                result.push(elem.ID);
            });

            RealizationTimeService.sort(result).then(function (data) {
                $scope.sortChange = false;
            })
        };

        $scope.remove = function (elem) {
            RealizationTimeService.remove(elem).then(function (data) {
                var idx = _.findIndex($scope.realizationTimes, {ID: elem.ID});
                if (idx > -1) {
                    $scope.realizationTimes.splice(idx, 1);
                    Notification.success($filter('translate')('removed') + " " + elem.name);
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            })
        };

        $scope.saveWorkingHours = function() {

            if( this.workingHoursForm ) {

                PsWorkingHourService.update(this.workingHoursForm).then( function(saved) {
                    if( saved.response ) {
                        Notification.success($filter('translate')('success'));
                    } else {
                        Notification.error($filter('translate')('error'));
                    }
                }, function() {
                    Notification.error($filter('translate')('error'));
                });

            }

        };

    });