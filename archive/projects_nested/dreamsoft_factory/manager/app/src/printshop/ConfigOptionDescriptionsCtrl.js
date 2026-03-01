angular.module('digitalprint.app')
    .controller('printshop.ConfigOptionDescriptionsCtrl', function ($scope, $filter, $rootScope, getData, Notification, PsConfigOptionService) {

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
        function loadData(){
            ConfigOptionService.getOptionDescriptions(currentOptID).then(function (data) {
                $scope.optionDescriptions = data;
            });
        }
        loadData();

        $scope.save = function () {
            var items=$scope.optionDescriptions;
            ConfigOptionService.saveOptionDescriptions(currentOptID, items).then(function (data) {
                Notification.success($filter('translate')('success'));
                loadData();
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

    });
