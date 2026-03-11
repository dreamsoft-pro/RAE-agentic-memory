import api from '@/lib/api';
import _ from 'lodash';

class ComplexProductManager {
    private selectedProduct: any;

    constructor(private baseProduct: any) {}

    public async initializeSelectedProduct(complexProduct: any): Promise<void> {
        const copyBaseProduct = _.clone(this.baseProduct);
        complexProduct.selectedProduct = copyBaseProduct;
        complexProduct.selectedProduct.data = {
            info: _.clone(copyBaseProduct),
            selectedOptions: {},
            attrPages: {},
            attributes: {},
            attributeMap: [],
            optionMap: {},
            currentFormat: false,
            currentPages: false,
            excludedOptions: [],
            formatExcluded: [],
            thickness: {
                values: {},
                min: null,
                max: null,
                current: null
            }
        };
    }

    public async addSelectedProductFormats(complexProduct: any, formats: any[]): Promise<void> {
        complexProduct.selectedProduct.data.formats = formats;
    }
}