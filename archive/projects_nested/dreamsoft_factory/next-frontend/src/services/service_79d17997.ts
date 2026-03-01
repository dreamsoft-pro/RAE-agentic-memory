import axios from 'axios';
import _ from 'lodash';

class ProductHandler {
    async prepareProductPromise(scope: any, newItem: any): Promise<void> {
        const def = { resolve: (value?: any) => {}, reject: (reason?: any) => {} } as { resolve: Function; reject: Function };
        
        newItem.products = [];
        _.each(scope.complexProducts, async (complexProduct, index) => {
            try {
                const product = complexProduct.selectedProduct.data;
                
                const newProduct: { options: Array<{ attrID: number; optID: string }> } = { options: [] };
                const emptyOptions = this.markEmptyOptions(product);
                
                _.each(product.selectedOptions, (optID, attrID) => {
                    if (!optID) {
                        console.log('Lack of optID:', optID);
                        console.log('attrID is:', attrID);
                    } else if (!_.includes(emptyOptions, optID)) {
                        newProduct.options.push({
                            attrID: parseInt(attrID),
                            optID: optID
                        });
                    }
                });

                newItem.products.push(newProduct);

            } catch (error) {
                def.reject(error);
            }
        }).then(() => {
            def.resolve();
        });
    }

    private markEmptyOptions(product: any): Array<string> {
        // Your implementation for marking empty options goes here
        return [];
    }
}