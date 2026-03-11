import { defer } from 'lodash';
import api from '@/lib/api';

class ProductChecker {
    private activeAttrID: number;

    constructor(activeAttrID: number) {
        this.activeAttrID = activeAttrID;
    }

    public async checkAttributeSelection(product: any): Promise<boolean> {
        return new Promise((resolve, reject) => {
            const deferred = defer();

            product.attributeMap.forEach(attribute => {
                if (attribute === this.activeAttrID) {
                    deferred.resolve(true);
                }
            });

            if (product.attributeMap.length === 0) {
                deferred.reject(false);
            }

            deferred.promise.then(resolve).catch(reject);
        });
    }

    public async checkAttrSelectAsync(product: any): Promise<boolean> {
        const deferred = defer();

        let firstFilteredOption = null;

        // Example logic to find the first filtered option
        for (const attr of product.attributeMap) {
            if (this.isFiltered(attr)) {  // Assume isFiltered is a method defined elsewhere
                firstFilteredOption = attr;
                break;
            }
        }

        // Further business logic based on firstFilteredOption

        return deferred.promise.then(() => true).catch(() => false);
    }

    private isFiltered(attribute: any): boolean {
        // Implement this method according to your criteria for filtering attributes
        return attribute.someCriteria;  // Replace with actual condition
    }
}