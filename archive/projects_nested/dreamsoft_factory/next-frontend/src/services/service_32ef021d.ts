import api from '@/lib/api';
import _ from 'lodash';

export default class MyClass {
    private tmpExclusions: Record<string, any> = {};

    public async processItem(item: { exclusions?: Array<any>; }, exclusionsThickness: Record<string, any>, exclusionsThicknessPages: Record<string, any>): Promise<void> {
        if (item.exclusions) {
            this.tmpExclusions = _.merge({}, item.exclusions, exclusionsThickness, exclusionsThicknessPages);
        }

        if (this.tmpExclusions) {
            // Your further logic using tmpExclusions can go here
        }
    }
}