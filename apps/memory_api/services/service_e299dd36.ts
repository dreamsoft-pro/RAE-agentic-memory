import api from '@/lib/api';
import _ from 'lodash';

interface Product {
    selectedOptions: { [attrID: number]: any };
    excludedOptions: string[];
}

interface Option {
    ID: number;
}

class ProductService {
    private async getAttributeFromOption(product: Product, optId: number): Promise<number> {
        // Business logic to fetch attribute from option
        const actAttrID = await api.getAttributeFromOption(product, optId);
        return actAttrID;
    }

    private async processOptions(attribute: { options: Option[]; filteredOptions: Option[] }, product: Product) {
        const allExclude: string[] = ['someValue']; // Example value, replace with actual implementation
        const deletedAttrs: number[] = [];

        for (const opt of attribute.options) {
            if (_.includes(allExclude, opt.ID)) {
                const actAttrID = await this.getAttributeFromOption(product, opt.ID);
                if (actAttrID > 0 && _.indexOf(deletedAttrs, actAttrID) === -1) {
                    delete product.selectedOptions[actAttrID];
                    deletedAttrs.push(actAttrID);
                }
            }
        }

        attribute.filteredOptions = _.filter(attribute.options, opt => !_.includes(product.excludedOptions, opt.ID));
    }

    public async getPreparedProduct(scope: any, selectedProduct: Product, amount: number, volume: number): Promise<Product> {
        const def = { resolve: (value?: boolean) => {}, promise: new Promise((resolve, reject) => {}) };

        try {
            await this.processOptions({ options: [], filteredOptions: [] }, selectedProduct);
            def.resolve(true);

            return def.promise;
        } catch (error) {
            console.error('Error preparing product:', error);
            def.reject(error);
            throw error;
        }
    }
}