import api from '@/lib/api';
import _ from 'lodash';

class MyClass {
    private type: any;

    constructor(type: any) {
        this.type = type;
    }

    public async getMinPages(): Promise<number> {
        if (!_.keys(this.type.thickness.values).length || !this.type.thickness.min) {
            const minPages = await this.getMinPagesInternal();
            return Math.max(minPages, (this.type.pages[0]?.minPages ?? 0));
        }

        let value = 0;
        _.values(this.type.thickness.values).forEach(one => {
            if (Number(one) > 0) {
                value += Number(one);
            }
        });

        return value;
    }

    private async getMinPagesInternal(): Promise<number> {
        // Implement the logic for getting min pages here.
        // For demonstration, returning a dummy value.
        return new Promise((resolve) => resolve(1));
    }
}

// Usage example:
const myInstance = new MyClass({ /* your type object */ });
myInstance.getMinPages().then(minPages => console.log(minPages));