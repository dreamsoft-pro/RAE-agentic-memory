import api from '@/lib/api';
import _ from 'lodash';

class CategoryChecker {
    private currentLang: string;

    constructor(currentLang: string) {
        this.currentLang = currentLang;
    }

    async checkMainCategory(items: any[]): Promise<any[]> {
        let types: any[] = [];
        
        if (_.isUndefined(items) || _.isEmpty(items)) {
            return [];
        }
        
        items.forEach(item => {
            let filtered: any[] = [];

            // Process child categories
            if (!_.isUndefined(item.childs) && !_.isNull(item.childs) && !_.isEmpty(item.childs)) {
                filtered = _.union(filtered, this.checkChilds(item.childs));
            }

            // Process groups
            if (!_.isUndefined(item.groups) && !_.isNull(item.groups) && !_.isEmpty(item.groups)) {
                filtered = _.union(filtered, this.checkGroups(item.groups));
            }

            // Directly add types if available
            if (!_.isUndefined(item.types) && !_.isNull(item.types) && !_.isEmpty(item.types)) {
                filtered = _.union(filtered, item.types);
            }
            
            filtered = _.sortBy(_.uniq(filtered, (item: any) => item.ID), (item: any): string | undefined => 
                this.getSortValue(item));

            types.push(...filtered);
        });

        types = this.removeDuplicates(types, 'ID');
        return types.sort((a: any, b: any) => a.name.localeCompare(b.name));
    }

    private checkChilds(childItems: any[]): any[] {
        let childTypes: any[] = [];
        
        if (_.isUndefined(childItems) || _.isEmpty(childItems)) {
            return [];
        }
        
        // Logic for processing children
        return childTypes;
    }

    private checkGroups(groupItems: any[]): any[] {
        let groupTypes: any[] = [];
        
        if (_.isUndefined(groupItems) || _.isEmpty(groupItems)) {
            return [];
        }
        
        // Logic for processing groups
        return groupTypes;
    }

    private removeDuplicates(arr: any[], key: string): any[] {
        const uniqueSet = new Set();
        return arr.filter(item => !uniqueSet.has((item[key] as unknown) as number) && uniqueSet.add((item[key] as unknown) as number));
    }

    private getSortValue(item: any): string | undefined {
        if (item.names != undefined && this.currentLang != undefined) {
            return item.names[this.currentLang];
        }
        return item.name;
    }
}