angular.module('digitalprint.app')
    .controller('shop.CouriersCtrl', function ($scope, $filter, $modal, ModuleService,
                                               ModuleValueService, Notification) {

        $scope.couriers = [];

        $scope.refresh = function () {
            ModuleService.getExtended('couriers').then(function (data) {
                $scope.couriers = data;
                console.log(data);
            });
        };

        $scope.refresh();

        $scope.save = function (module) {
            var courier = {keys: {}, 'moduleID': module.ID};
            _.each(module.keys, function (key) {
                courier.keys[key.ID] = key.value;
            });

            var ValueService = new ModuleValueService(module.key);

            ValueService.update(courier).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                console.log(data);
                Notification.error($filter('translate')('error'));
            });
        };

    });