javascript
'use strict';

angular.module('dpClient.app')
    .controller('index.SearchCtrl', function($rootScope, $scope, $state, $filter,
                                             Notification, PsTypeService, $stateParams) {

    // [BACKEND_ADVICE] Extract initialization logic to a separate method.
    
    var searchText = $stateParams.text;
    $scope.searchText = searchText;

    function init() {
        PsTypeService.search(searchText).then(function(data) {
            $scope.results = data;
        });
    }

    function initializeSearch() {
        init();
    }

    initializeSearch();

});
