import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class ProductHelper {
    private async handleProductSelection(product: any, attrID: string, attributeIndex: number, index: number): Promise<boolean> {
        const def = { resolve: (value: boolean) => {}, promise: new Promise((resolve) => def.resolve = resolve) };

        if (!product.selectedOptions[attrID]) {
            if ((product.attributeMap.length - 1) > index) {
                def.resolve(true);
            }
        } else {
            if (attributeIndex > -1 && product.attributes[attributeIndex].filteredOptions.length === 0) {
                delete product.selectedOptions[attrID];
            }

            if ((product.attributeMap.length - 1) > index) {
                def.resolve(true);
            }
        }

        index++;
        return def.promise;
    }

    public async markEmptyOptions(product: any): Promise<void> {
        // Implement your logic here using the handleProductSelection method
    }
}