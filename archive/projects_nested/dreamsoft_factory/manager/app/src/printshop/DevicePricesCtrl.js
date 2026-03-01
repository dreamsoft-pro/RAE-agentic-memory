angular.module('digitalprint.app')
    .controller('printshop.DevicePricesCtrl', function ($scope, $filter, $modal, DeviceService, Notification,
                                                        DepartmentService, $stateParams) {
        $scope.deviceID = $stateParams.deviceID;

        DeviceService.get($scope.deviceID).then(function(data){
            $scope.deviceName=data.name;
        });

       function getAll(){
           DeviceService.getPrices($scope.deviceID).then(function(data){
               $scope.prices=data;
           });
       }
        getAll();
        $scope.addPrice=function(){
            DeviceService.addPrice($scope.deviceID, $scope.form).then(function(data){
                    Notification.success($filter('translate')('success'));
                    $scope.resetPriceForm();
                    getAll();
            }, function(data){
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };
        $scope.resetPriceForm=function(){
            $scope.form={};
        };
        $scope.resetPriceForm();
        $scope.deletePrice=function(priceID){
            DeviceService.deletePrice($scope.deviceID, priceID).then(function(data){
                Notification.success($filter('translate')('success'));
                getAll();
            }, function(data){
                    Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
                });
        };

    });
