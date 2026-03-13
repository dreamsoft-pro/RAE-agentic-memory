import api from '@/lib/api';
import _ from 'lodash'; // Assuming lodash is being used for utility functions

interface Product {
    attributeMap: string[];
    attributes: any[];
    excludedOptions: number[];
    selectedOptions: number[];
}

class ProductController {
    private async setOptionExclusionsAsync(product: Product, attrID: string, exclusions: number[][]): Promise<boolean> {
        let deletedAttrs = [];
        
        const attribute = _.find(product.attributes, { attrID });

        if (!attribute) {
            throw new Error(`Attribute with ID ${attrID} not found`);
        }

        const allExclude = [];
        for (const exc of exclusions) {
            for (const optID of exc) {
                allExclude.push(optID);
                product.excludedOptions.push(optID);

                _.each(product.selectedOptions, selectedOptID => {
                    // Business logic to handle selected options
                });
            }
        }

        if (_.last(product.attributeMap) === attrID) {
            return true;
        } else {
            return false;
        }
    }
}