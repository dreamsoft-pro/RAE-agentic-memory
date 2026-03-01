javascript
import '@/lib/api';
import _ from 'lodash';

function checkMainCategory(items) {
    var types = [];
    
    // [BACKEND_ADVICE] Check if items is undefined or empty
    if (_.isUndefined(items) || _.isEmpty(items)) {
        return [];
    }

    _.each(items, function (item) {
        let filtered = [];

        // [BACKEND_ADVICE] Process item.childs
        if (!_.isUndefined(item.childs) && !_.isNull(item.childs) && !_.isEmpty(item.childs)) {
            filtered = _.union(filtered, checkChilds(item.childs));
        }

        // [BACKEND_ADVICE] Process item.groups
        if (!_.isUndefined(item.groups) && !_.isNull(item.groups) && !_.isEmpty(item.groups)) {
            filtered = _.union(filtered, checkGroups(item.groups));
        }

        // [BACKEND_ADVICE] Process item.types
        if (!_.isUndefined(item.types) && !_.isNull(item.types) && !_.isEmpty(item.types)) {
            filtered = _.union(filtered, item.types);
        }

        // [BACKEND_ADVICE] Sort and remove duplicates from filtered array based on ID
        filtered = _.sortBy(_.uniq(filtered, function (item) {
            return item.ID;
        }), function(item) {
            if (!_.isUndefined(item.names[$rootScope.currentLang.code])) {
                return item.names[$rootScope.currentLang.code];
            }
            return item.name;
        });

        types.push.apply(types, filtered);
    });

    // [BACKEND_ADVICE] Remove duplicates from the main array based on ID
    types = removeDuplicates(types, "ID");

    // [BACKEND_ADVICE] Final sort based on name
    return types.sort(function(a, b) {
        if (a.name < b.name) return -1;
        if (a.name > b.name) return 1;
        return 0;
    });
}

function checkChilds(childItems) {
    // [BACKEND_ADVICE] Implement logic for processing child items
    return [];
}

function checkGroups(groupItems) {
    // [BACKEND_ADVICE] Implement logic for processing group items
    return [];
}

function removeDuplicates(array, key) {
    // [BACKEND_ADVICE] Remove duplicates from the array based on a specific key
    const seen = new Set();
    return array.filter(item => !seen.has(item[key]) && seen.add(item[key]));
}
