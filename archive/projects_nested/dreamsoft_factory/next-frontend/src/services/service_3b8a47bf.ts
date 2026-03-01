import axios from 'axios';
import _ from 'lodash';

class ProductHelper {

    private product: any;

    constructor(initialProduct: any) {
        this.product = initialProduct;
    }

    getEmptyOptions(): string[] {
        const emptyOptions: string[] = [];
        _.each(this.product.selectedOptions, (optID: string, attrID: number) => {
            const idx = _.findIndex(this.product.attributes, {attrID: parseInt(attrID)});
            if (idx > -1 && this.product.attributes[idx].filteredOptions.length === 0) {
                emptyOptions.push(optID);
            }
        });
        return emptyOptions;
    }

    removeEmptyOptionFromSelected(newProduct: any): void {
        const emptyOptions = this.getEmptyOptions();
        newProduct.selectedOptions = _.omitBy(newProduct.selectedOptions, (value, key) => emptyOptions.includes(key));
    }
}