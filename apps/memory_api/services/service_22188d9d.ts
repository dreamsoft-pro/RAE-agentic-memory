import axios from 'axios';
import * as _ from 'lodash';

type ProductAttribute = {
    attrID: string;
};

type Option = {
    ID: string;
    formats?: string[];
};

type Product = {
    attributes: ProductAttribute[];
    attributeMap: Record<string, any>;
    currentFormat: { ID: string };
    selectedOptions: Record<string, string>;
    formatExcluded: string[];
    selectedID: string | null;
};

async function processProductAttributes(product: Product): Promise<void> {
    for (const attrID of Object.values(product.attributeMap)) {
        const attributeIndex = _.findIndex(product.attributes, { attrID });
        if (attributeIndex === -1) continue;

        let optionIndex = 0;
        const attribute = product.attributes[attributeIndex];
        
        for (const option of attribute.options) {
            if (option.formats && !_.includes(option.formats, product.currentFormat.ID)) {
                product.formatExcluded.push(option.ID);
                
                if (product.selectedOptions[attrID] === option.ID) {
                    delete product.selectedOptions[attrID];
                }
            }

            if ((attributeIndex + 1) === product.attributes.length && (optionIndex + 1) === attribute.options.length) {
                return;
            }

            optionIndex++;
        }
    }
}

function removeUnActiveOptions(product: Product): void {
    processProductAttributes(product).then(() => {
        // Handle resolved promise here if necessary
    });
}