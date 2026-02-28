angular.module('digitalprint.app')
    .controller('printshop.ConfigOptionRealizationTimesCtrl', function ($scope, $filter, $rootScope, getData, Notification,
                                                                        PsConfigOptionService) {

        var currentAttrID = $scope.currentAttrID = getData.currentAttrID;
        var currentOptID = $scope.currentOptID = getData.currentOptID;

        $scope.option = angular.copy(getData.option);
        $scope.attr = getData.attribute;
        $scope.menu = getData.menu;
        $scope.prevOption= getData.prevOption;
        $scope.nextOption= getData.nextOption;
        $rootScope.currentAttrName = getData.attribute.name;
        $rootScope.currentOptionName = getData.option.name;

        var ConfigOptionService = new PsConfigOptionService(currentAttrID);

        ConfigOptionService.getRealizationTimes(currentOptID).then(function (data) {
            $scope.realizationTimes = data;
        });

        $scope.add = function () {
            ConfigOptionService.addRealizationTime(currentOptID, $scope.form).then(function (data) {
                var idx = _.findIndex($scope.realizationTimes, {ID: data.ID});
                if (idx > -1) {
                    $scope.realizationTimes[idx] = data;
                } else {
                    $scope.realizationTimes.push(data);
                }
                $scope.resetForm();
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.remove = function (item) {
            ConfigOptionService.removeRealizationTime(currentOptID, item).then(function (data) {
                var idx = _.findIndex($scope.realizationTimes, {ID: item.ID});
                if (idx > -1) {
                    $scope.realizationTimes.splice(idx, 1);
                }
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.resetForm = function () {
            $scope.form = {};
        }


    });
