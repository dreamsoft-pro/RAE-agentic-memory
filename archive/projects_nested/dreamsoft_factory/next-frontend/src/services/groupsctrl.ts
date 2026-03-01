javascript
'use strict';

angular.module('dpClient.app')
	.controller('category.GroupsCtrl', function($scope, $rootScope, $filter, $q, PsTypeService, PsGroupService,
                                                DpCategoryService, PsGroupDescriptionService, $stateParams,
                                                Notification, MainWidgetService) {

    var currentGroupID;
    var currentGroupUrl;

    $scope.descriptions = [];
    $scope.galleries = [];

    function init() {
        $scope.items = [];
        $scope.group = {};
        $scope.category = {};
        $scope.form = {};
        currentGroupUrl = $stateParams.groupurl;
        getTypes(currentGroupUrl);
        getGroup(currentGroupUrl);
        DpCategoryService.getOne($stateParams.categoryurl).then(function(category) {
            $scope.category = category;
            getDescription(currentGroupUrl);
        });
    }

    function getTypes(groupUrl) {
        PsTypeService.getTypesForGroup(groupUrl).then(function(types) {
            $scope.types = types;
        });
    }

    function getGroup(groupUrl) {
        PsGroupService.getGroupByUrl(groupUrl).then(function(group) {
            currentGroupID = group.id;
            $scope.group = group;
        });
    }

    init();
});
