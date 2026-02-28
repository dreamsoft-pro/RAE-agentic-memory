javascript
'use strict';

angular.module('dpClient.app')
    .controller('client-zone.CreateReclamationCtrl', function ($q, $scope, $rootScope, Notification, $filter,
                                                               ReclamationService, FileUploader, AuthDataService,
                                                               $stateParams, DpProductService, MainWidgetService,
                                                               $config) {

// [BACKEND_ADVICE] Initialize scope variables and set orderID from stateParams
    $scope.faults = [];
    $scope.uploadProgress = 0;
    $scope.orderID = $stateParams.orderid;
    $scope.form = {};
    $scope.reclamationExist = false;
    $scope.reclamation = {};
    $scope.products = [];

    const accessTokenName = $config.ACCESS_TOKEN_NAME;

// [BACKEND_ADVICE] Set authorization header using access token
    const header = {};
    header[accessTokenName] = AuthDataService.getAccessToken();
