angular.module('digitalprint.app')
    .controller('printshop.ConfigOptionEditCtrl', function ($scope, $filter, $rootScope, getData, Notification, PsConfigOptionService) {

        var currentAttrID = $scope.currentAttrID = getData.currentAttrID;
        var currentOptID = $scope.currentOptID = getData.currentOptID;

        $scope.option = angular.copy(getData.option);
        $scope.form = getData.option;
        $scope.attr = getData.attribute;
        $scope.menu = getData.menu;
        $scope.prevOption= getData.prevOption;
        $scope.nextOption= getData.nextOption;
        $rootScope.currentAttrName = getData.attribute.name;
        $rootScope.currentOptionName = getData.option.name;

        var ConfigOptionService = new PsConfigOptionService(currentAttrID);

        $scope.specialFunctionsList = [
            {
                name: 'Kadrowanie',
                value: 'crop',
                ID: 'crop'
            },
            {
                name: 'Preflight manual',
                value: 'prefManual',
                ID: 'prefManual'
            }];

        $scope.resetForm = function () {
            $scope.form = angular.copy($scope.option);
        };

        $scope.save = function () {
            ConfigOptionService.edit($scope.form).then(function (data) {
                $scope.option = angular.copy($scope.form);
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

    });
