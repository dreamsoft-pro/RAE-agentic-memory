import { filter, includes, first } from 'lodash';
import api from '@/lib/api';

class ProductAttributeManager {
    async processAttributes(product: any, deletedAttrs: string[]): Promise<void> {
        for (const attribute of product.attributes) {
            if (includes(deletedAttrs, attribute.attrID)) {
                const selectedOptions = attribute.attrID in product.selectedOptions ? product.selectedOptions : {};
                
                if (selectedOptions[attribute.attrID]) {
                    const firstFilteredOption = first(attribute.filteredOptions);
                    if (firstFilteredOption) {
                        product.selectedOptions[attribute.attrID] = firstFilteredOption.ID;
                    }
                } else {
                    attribute.filteredOptions = filter(attribute.options, opt => !includes(product.excludedOptions || [], opt.ID));
                    
                    const firstFilteredOption = first(attribute.filteredOptions);
                    if (firstFilteredOption) {
                        selectedOptions[attribute.attrID] = firstFilteredOption.ID;
                        product.selectedOptions = { ...product.selectedOptions, [attribute.attrID]: firstFilteredOption.ID };
                    }
                }
            }
        }
    }
}

// Usage example
const manager = new ProductAttributeManager();
manager.processAttributes(product, deletedAttrs).catch(console.error);