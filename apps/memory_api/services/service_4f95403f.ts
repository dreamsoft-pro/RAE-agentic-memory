import api from '@/lib/api';
import _ from 'lodash';

export default class ComplexProductHandler {
    private complexProduct: any;
    private attrID: number;

    constructor(complexProduct: any, attrID: number) {
        this.complexProduct = complexProduct;
        this.attrID = attrID;
    }

    async showOption(): Promise<string> {
        const resource = 'complexProducts';
        const url = `/api/${resource}`;
        
        let attrIdx = _.findIndex(this.complexProduct.selectedProduct.data.attributes, { attrID: parseInt(this.attrID) });
        if (attrIdx === -1) return '';

        const attribute = this.complexProduct.selectedProduct.data.attributes[attrIdx];
        const optID = this.complexProduct.selectedProduct.data.selectedOptions[attribute.attrID];

        let optIdx = _.findIndex(attribute.filteredOptions, { ID: parseInt(optID) });
        if (optIdx === -1) return '';

        const option = attribute.filteredOptions[optIdx];
        
        if (option.invisible === 1) {
            return '';
        }

        // Example of making an API call
        try {
            const response = await api.get(url);
            console.log(response.data);
        } catch (error) {
            console.error('Error fetching resource:', error);
        }
        
        return option.name;
    }
}