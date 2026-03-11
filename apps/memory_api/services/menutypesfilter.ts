javascript
'use strict';

angular.module('dpClient.app').filter('menutypes', function ($rootScope) {
    function checkChilds(childs) {
        var filtered = [];
        _.each(childs, (child) => {
            if (!_.isUndefined(child.groups) && !_.isNull(child.groups) && !_.isEmpty(child.groups)) {
                filtered = _.union(filtered, checkGroups(child.groups));
            }
            if (!_.isUndefined(child.types) && !_.isNull(child.types) && !_.isEmpty(child.types)) {
                filtered = _.union(filtered, child.types);
            }
        });
        return filtered;
    }

    function checkGroups(groups) {
        var filtered = [];
        _.each(groups, (group) => {
            if (!_.isNull(group) && !_.isUndefined(group.types) && !_.isEmpty(group.types)) {
                filtered = _.union(filtered, group.types);
            }
        });
        return filtered;
    }

    return function filterMenutypes(input) {
        var result = [];
        if (input && input.length > 0) {
            result = checkChilds(input);
        }
        return result;
    };
});
