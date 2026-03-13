/**
 * Created by Rafał on 31-08-2017.
 */
angular.module('digitalprint.app')
    .controller('contents.ReclamationsCtrl', function ($scope, $rootScope, $filter, $modal, Notification,
                                                             ReclamationFaultService, SettingService) {
        $scope.faults = [];

        var settings = new SettingService('reclamation');

        $scope.settingForm = {
            reclamationDays: {
                value: ''
            }
        };

        function init() {
            ReclamationFaultService.getFaults().then(function( faultsData ) {
                $scope.faults = faultsData;
            });
        }

        $scope.add = function() {
            ReclamationFaultService.addFault(this.form).then(function(data) {
                if( data.response === true ){
                    $scope.form = {};
                    $scope.faults.push(data.item);
                    Notification.success($filter('translate')('added')+" "+data.item.key);
                }
            });
        };

        $scope.remove = function( fault ) {
            ReclamationFaultService.removeFault(fault.ID).then(function(data) {
                if( data.response === true ) {
                    var idx = _.findIndex($scope.faults, {ID: data.item.ID});
                    if( idx > -1 ) {
                        $scope.faults.splice(idx, 1);
                        Notification.success($filter('translate')('removed') + " " + data.item.ID);
                    }
                }
            });
        };

        $scope.edit = function (item) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/edit-reclamation-fault.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = _.clone(item, true);
                    $scope.save = function () {
                        ReclamationFaultService.editFault(this.form).then( function(data) {
                            if( data.response === true ) {
                                var idx = _.findIndex($scope.faults, {ID: data.item.ID});
                                if( idx > -1 ) {
                                    $scope.faults[idx] = data.item;
                                }
                                Notification.success($filter('translate')('saved'));
                                $modalInstance.close();
                            } else {
                                Notification.error($filter('translate')('error'));
                            }

                        })
                    }
                }
            });
        };

        $scope.saveSettings = function () {
            settings.setModule('reclamation');
            settings.save($scope.settingForm).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        init();
    });