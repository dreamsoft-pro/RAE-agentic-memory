import api from "@/lib/api";
import _ from "lodash";

class ProductHelper {

    async fetchProductExclusions(productId: string): Promise<Record<string, string[]>> {
        const product = await api.get(`/api/products/${productId}`);
        
        const exclusions: Record<string, string[]> = {};

        _.forEach(product.attributes, (attribute) => {
            if (!exclusions[attribute.attrID]) {
                exclusions[attribute.attrID] = [];
            }

            _.forEach(attribute.options, (option) => {
                let resource = 'your-resource';
                let url = `/api/options/${option.ID}`;
                
                const idx = product.excludedOptions.indexOf(option.ID);

                if (idx === -1) {
                    exclusions[attribute.attrID].push(option.ID);
                }
            });
        });

        return exclusions;
    }

    countAttrNotExcludedOptions(product: any, attr: any): number {
        let count = 0;

        _.each(attr.options, (option) => {
            if (!_.includes(product.excludedOptions, option.ID)) {
                count++;
            }
        });

        return count;
    }
}

export default ProductHelper;