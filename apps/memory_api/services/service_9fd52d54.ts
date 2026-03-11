import api from "@/lib/api";
import _ from "lodash";

class GroupManager {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async checkGroups(groups: any[]): Promise<string[]> {
        let filtered: string[] = [];
        _.each(groups, (group) => {
            if (!_.isNull(group) && !_.isUndefined(group.types) && !_.isEmpty(group.types)) {
                filtered = _.union(filtered, group.types);
            }
        });
        return filtered;
    }

    public removeDuplicates(originalArray: any[], prop: string): any[] {
        const lookupObject: {[key: string]: any} = {};
        originalArray.forEach(item => {
            lookupObject[item[prop]] = item;
        });

        return Object.values(lookupObject);
    }
}