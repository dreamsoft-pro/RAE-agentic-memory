import api from '@/lib/api';

class ProductHandler {
    private resource: string;
    private url: string;

    constructor(resource: string, url: string) {
        this.resource = resource;
        this.url = url;
    }

    async handleProductSelection(indexFormat: number, product: any, oneProduct: any): Promise<void> {
        if (indexFormat > -1) {
            if (product.calcProducts[indexFormat].customFormat) {
                oneProduct.formats[indexFormat].custom = 1;
                oneProduct.formats[indexFormat].customWidth = product.calcProducts[indexFormat].formatWidth;
                oneProduct.formats[indexFormat].customHeight = product.calcProducts[indexFormat].formatHeight;
            }
            await this.selectFormat(oneProduct, oneProduct.formats[indexFormat], true);
        }

        return Promise.resolve(true);
    }

    private async selectFormat(product: any, format: any, isCustom: boolean): Promise<void> {
        // Implement the logic for selecting a format based on the product and format details.
        // Use this.resource and this.url as needed to interact with the API or server.
    }

    getMinPages(type: { minOptionPages: Record<string, number> }): number | false {
        if (Object.keys(type.minOptionPages).length > 0) {
            return Math.min(...Object.values(type.minOptionPages));
        }
        return false;
    }

    getOption(product: any, optID: string): any {
        // Implement the logic for getting an option based on product and optID.
        // Use this.resource and this.url as needed to interact with the API or server.
    }
}