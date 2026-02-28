angular.module('digitalprint.app')
    .controller('customerservice.CreateOrderTypesCtrl', function ($scope, $state, $stateParams, PsGroupService,
                                                                  PsTypeService, Notification, UserService,
                                                                  CustomProductService, typeOfResource, $filter) {

        $scope.types = [];
        var currentProductID = $stateParams.groupID;
        var currentUserID = $stateParams.userID;
        var customProductID = $state.params.customProductID;

        $scope.typeOfResource = typeOfResource;

        $scope.customProduct = false;

        function init() {

            if( customProductID ) {

                CustomProductService.getOne(customProductID).then( function( customProductData ) {
                    $scope.customProduct = customProductData;
                });

            }

            PsGroupService.get(currentProductID).then(function (data) {
                $scope.group = data;
            }, function (data) {
                Notification.error($filter('translate')('data_retrieve_failed'));
            });

            PsTypeService.getActiveTypes(currentProductID).then(function (data) {
                $scope.types = data;
                if ($scope.types.length === 1) {
                    $scope.selectType($scope.types[0]);
                }
            }, function (data) {
                Notification.error($filter('translate')('data_retrieve_failed'));
            });

            UserService.getUser(currentUserID).then(function (userInfo) {
                $scope.orderOwner = userInfo;
            });
        }

        $scope.selectType = function (type) {
            if(typeOfResource.type === 'offer') {
                $state.go('create-offer-calc', {userID: currentUserID, groupID: currentProductID, typeID: type.ID});
            } else if ( typeOfResource.type === 'order' ) {
                $state.go('create-order-calc', {userID: currentUserID, groupID: currentProductID, typeID: type.ID});
            }
        };

        $scope.goToProducts = function () {
            $state.go('create-order', {userID: currentUserID});
        };

        init();

    });