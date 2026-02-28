import api from '@/lib/api';
import _ from 'lodash';

export default class MenuTypesService {
    private $rootScope: any; // Assuming this is passed as a parameter

    constructor($rootScope: any) {
        this.$rootScope = $rootScope;
    }

    public checkChilds(childs: any[]): any[] {
        let filtered: any[] = [];
        _.each(childs, (child: any) => {
            if (!_.isUndefined(child.groups) && !_.isNull(child.groups) && !_.isEmpty(child.groups)) {
                filtered = _.union(filtered, this.checkGroups(child.groups));
            }
            if (!_.isUndefined(child.types) && !_.isNull(child.types) && !_.isEmpty(child.types)) {
                filtered = _.union(filtered, child.types);
            }
        });
        return filtered;
    }

    private checkGroups(groups: any[]): any[] {
        let result: any[] = [];
        _.each(groups, (group: any) => {
            if (!_.isUndefined(group.children) && !_.isNull(group.children) && !_.isEmpty(group.children)) {
                result = _.union(result, this.checkChilds(group.children));
            }
            // Add logic for other properties of group here
        });
        return result;
    }
}