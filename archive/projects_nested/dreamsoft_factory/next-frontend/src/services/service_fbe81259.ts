import api from '@/lib/api';
import _ from 'lodash';

class ProductProcessor {
    async processSelectedProduct(selectedProductData: any, newItem: any): Promise<void> {
        const newProduct = { pages: 0, options: [], attrPages: {} };

        if (selectedProductData.currentPages) {
            newProduct.pages = selectedProductData.currentPages;
        } else {
            newProduct.pages = 2;
        }

        _.each(selectedProductData.selectedOptions ?? {}, (optID: any, attrID: string) => {
            if (!optID) {
                console.log('Lack of optID:', optID);
                console.log('attrID is:', attrID);
            } else {
                newProduct.options.push({
                    attrID: parseInt(attrID),
                    optID
                });
            }
        });

        newProduct.attrPages = selectedProductData.attrPages ?? {};

        newItem.products.push(newProduct);
    }
}