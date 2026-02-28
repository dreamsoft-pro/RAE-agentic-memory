javascript
'use strict';

const { configureRoutes } = require('@/lib/api');

angular.module('dpClient.routes').config(['$locationProvider', '$stateProvider', '$urlRouterProvider', function($locationProvider, $stateProvider) {
    // [BACKEND_ADVICE] Configure route logic here.
    configureRoutes($locationProvider, $stateProvider);
}]);
