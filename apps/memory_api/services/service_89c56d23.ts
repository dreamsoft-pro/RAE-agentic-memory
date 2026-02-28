import api from '@/lib/api';

class ProductAttributes {
    private complexProduct: any;
    private attrID: number;

    constructor(complexProduct: any, attrID: string) {
        this.complexProduct = complexProduct;
        this.attrID = parseInt(attrID);
    }

    public async showAttribute(): Promise<string> {
        const attributeIndex = this.getAttributeIndex();
        
        if (attributeIndex > -1) {
            const attribute = this.complexProduct.selectedProduct.data.attributes[attributeIndex];
            const optionId = complexProduct.selectedProduct.data.selectedOptions[attribute.attrID];

            const optionIndex = this.getOptionIndex(attribute, optionId);
            
            if (optionIndex > -1) {
                const option = attribute.filteredOptions[optionIndex];

                if (option.invisible === 1) {
                    return '';
                }
            }
        }

        // Assuming the original logic returned some default value or handled not found cases.
        return ''; // Placeholder for actual business logic
    }

    private getAttributeIndex(): number {
        return this.complexProduct.selectedProduct.data.attributes.findIndex(attr => attr.attrID === this.attrID);
    }

    private getOptionIndex(attribute: any, optionId: string): number {
        return attribute.filteredOptions.findIndex(opt => opt.ID === parseInt(optionId));
    }
}

export default ProductAttributes;