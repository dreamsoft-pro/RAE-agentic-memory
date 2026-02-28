import api from "@/lib/api";
import _ from "lodash";

export default class ProductHelper {
    private item: any;

    constructor() {
        this.item = undefined;
    }

    public async getItem(product: any, optID: number): Promise<any> {
        let resource: string[] = product.attributes;

        for (const attribute of resource) {
            const idx = _.findIndex(attribute.options, { ID: optID });

            if (idx > -1) {
                this.item = attribute.options[idx];
                break;
            }
        }

        return this.item;
    }

    public setRangePages(product: any, attrID: number): void {
        let resource: any[] = product.attributes;

        const idx = _.findIndex(resource, { attrID });

        if (idx > -1) {
            if (product.attributes[idx].minPages !== null) {
                if (!product.attrPages[attrID]) {
                    product.attrPages[attrID] = product.attributes[idx].minPages;
                }
            }
        } else {
            console.error('Some functions may not work well.');
        }
    }

    public async setExclusionsAsync(scope: any, product: any): Promise<void> {
        // Placeholder for the actual asynchronous logic
        // As per rules, no RxJS is allowed, so this method needs to be refactored.
        return;
    }
}