'use strict';

angular.module('digitalprint.app')
    .controller('printshop.VolumesCtrl', function ($scope, $rootScope, $filter, $stateParams, Notification,
                                                   PsVolumeService, PsFormatService, $modal, getData) {
        var currentGroupID;
        var currentTypeID;

        currentGroupID = $scope.currentGroupID = $stateParams.groupID;
        currentTypeID = $scope.currentTypeID = $stateParams.typeID;

        $rootScope.currentTypeName = getData.type.name;
        $rootScope.currentGroupName = getData.group.name;

        $scope.maxVolume = getData.type.maxVolume;
        $scope.stepVolume = getData.type.stepVolume;

        var VolumeService = new PsVolumeService(currentGroupID, currentTypeID);

        VolumeService.getAll().then(function (data) {
            $scope.volumes = data;
        });

        $scope.refresh = function () {
            VolumeService.getAll(true).then(function (data) {
                $scope.volumes = data;
            });
        };

        VolumeService.getCustom().then(function (data) {
            $scope.customVolume = data.custom;
        });

        var FormatService = new PsFormatService(currentGroupID, currentTypeID);
        FormatService.getAll().then(function (data) {
            $scope.formats = data;
        });


        $scope.resetForm = function () {
            $scope.form = {};
        };

        $scope.resetForm();
        $scope.add = function (form) {

            VolumeService.add(form).then(function (data) {
                $scope.volumes.push(data);
                $scope.resetForm();
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.setCustomVolume = function () {
            VolumeService.setCustom($scope.customVolume).then(function (data) {

                Notification.success($filter('translate')('success'));
            });

        };

        $scope.setMaxVolume = function () {
            console.log($scope.maxVolume);
            VolumeService.setMaxVolume($scope.maxVolume).then(function (data) {
                Notification.success($filter('translate')('success'));
            });
        };
        $scope.setStepVolume = function () {
            VolumeService.setStepVolume($scope.stepVolume).then(function (data) {
                Notification.success($filter('translate')('success'));
            });
        };

        $scope.setInvisible = function (volume) {
            VolumeService.setInvisible(volume).then(function (data) {
                volume.invisible = !volume.invisible;
                Notification.success($filter('translate')('success'));
            });

        };

        $scope.volumeFormats = function (volume) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/volume-formats.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.volume = _.clone(volume);

                    _.each($scope.formats, function (item) {
                        if (_.indexOf(volume.formats, item.ID) > -1) {
                            item.selected = 1;
                        } else {
                            item.selected = 0;
                        }

                    });

                    $scope.save = function () {
                        volume.formats = [];

                        _.each($scope.formats, function (item) {
                            if (item.selected) {
                                volume.formats.push(item.ID);
                            }
                        });

                        VolumeService.setFormats(volume.ID, volume.formats).then(function (data) {
                            Notification.success($filter('translate')('success'));
                            $modalInstance.close();
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })
        };

        $scope.rtDetails = function (volume) {
            $modal.open({
                templateUrl: 'src/printshop/templates/realization-times-details.html',
                scope: $scope,
                controller: function ($scope, $modalInstance, realizationTimes) {
                    $scope.realizationTimes = realizationTimes;

                    $scope.editStart = function (item) {
                        $modal.open({
                            templateUrl: 'src/printshop/templates/modalboxes/edit-realizationtime-details.html',
                            scope: $scope,
                            controller: function ($scope, $modalInstance) {
                                $scope.form = {};
                                $scope.oryg = item;

                                $scope.form.pricePercentage = item.details ? item.details.pricePercentage : item.pricePercentage;
                                $scope.form.active = item.details ? item.details.active : item.active;
                                $scope.form.days = item.details ? item.details.days : item.days;
                                $scope.form.realizationID = item.ID;

                                $scope.save = function () {
                                    VolumeService.saveRtDetails(volume, $scope.form).then(function (data) {
                                        item.details = angular.copy($scope.form);
                                        item.details.ID = data.data.ID;
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
                        });
                    };


                    $scope.remove = function (item) {
                        VolumeService.removeRtDetails(volume, item).then(function (data) {
                            var idx = $scope.realizationTimes.indexOf(item);
                            if (idx > -1) {
                                delete $scope.realizationTimes[idx].details;
                            }
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }


                },
                resolve: {
                    realizationTimes: function ($q) {
                        var def = $q.defer();
                        VolumeService.getRtDetails(volume).then(function (data) {
                            def.resolve(data);
                        }, function (data) {
                            def.reject(data);
                        });

                        return def.promise;
                    }
                }
            })
        };

        $scope.remove = function (item) {
            VolumeService.remove(item).then(function (data) {
                var idx = _.findIndex($scope.volumes, {ID: item.ID});
                if (idx > -1) {
                    $scope.volumes.splice(idx, 1);
                    Notification.success($filter('translate')('success'));
                }

            });
        }


    });