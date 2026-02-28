angular.module('digitalprint.app')
    .controller('customerservice.CreateOrderGroupsCtrl', function ($scope, $rootScope, $state, $stateParams,
                                                                   PsGroupService, Notification, UserService,
                                                                   CustomProductService, typeOfResource,
                                                                   ApiCollection, $timeout) {

        $scope.groups = [];
        $scope.orderOwner = false;
        $scope.customProduct = false;

        $scope.typeOfResource = typeOfResource;

        var userID = $stateParams.userID;
        var customProductID = $state.params.customProductID;

        $scope.typesLimit = 10;

        var typesConfig = {
            params: {
                limit: $scope.typesLimit
            },
            onSuccess: function (data) {
                $scope.typesCollection.items = data;
            }
        };

        $scope.typeaheadObject ={
            query : '',
            lang: $rootScope.currentLang.code
        };

        $scope.typesCollection = new ApiCollection('ps_types/searchAll', typesConfig);

        var updateTableTimeout;

        $scope.findType = function (val, type) {
            $scope.typesCollection.params.search = val;
            $scope.typesCollection.params.type = type;
            $scope.typesCollection.params.active = 1;
            $timeout.cancel(updateTableTimeout);

            updateTableTimeout = $timeout(function () {
                return $scope.typesCollection.clearCache().then(function (data) {
                    $scope.typesCollection.items = data;
                    return data;
                });
            }, 300);
            return updateTableTimeout;
        };

        $scope.goToType = function() {
            if(typeOfResource.type === 'offer') {
                $state.go('create-offer-calc', {userID: userID, groupID: $scope.searchForm.type.groupID,
                    typeID: $scope.searchForm.type.ID});
            } else if ( typeOfResource.type === 'order' ) {
                $state.go('create-order-calc', {userID: userID, groupID: $scope.searchForm.type.groupID,
                    typeID: $scope.searchForm.type.ID});
            }
        };

        function init() {

            if( customProductID ) {

                CustomProductService.getOne(customProductID).then( function( customProductData ) {
                    $scope.customProduct = customProductData;
                });

            }

            PsGroupService.getActiveGroups().then(function (data) {
                $scope.groups = data;
                if ($scope.groups.length === 1) {
                    $scope.selectType($scope.groups[0]);
                }
            }, function (data) {
                Notification.error($filter('translate')('data_retrieve_failed'));
            });

            if( userID ) {
                UserService.getUser(userID).then(function (userInfo) {
                    $scope.orderOwner = userInfo;
                });
            } else {
                UserService.getLoggedUserData().then(function (userInfo) {
                    $scope.orderOwner = userInfo;
                });
            }

        }

        $scope.selectGroup = function (group) {
            $state.go('create-order-types', {'userID': userID, 'groupID': group.ID});
        };

        init();
    });