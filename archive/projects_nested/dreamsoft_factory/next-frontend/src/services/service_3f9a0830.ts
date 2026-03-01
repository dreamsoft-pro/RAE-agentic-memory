import api from '@/lib/api';

class ProductFormatHandler {
    private currentFormat: any;
    private relatedFormats: Array<any>;
    private product: { info: { typeID: number }, formats: Array<any>, relatedFormats?: Array<any> };

    constructor(currentFormat: any, relatedFormats: Array<any>, product: { info: { typeID: number }, formats: Array<any>, relatedFormats?: Array<any> }) {
        this.currentFormat = currentFormat;
        this.relatedFormats = relatedFormats;
        this.product = product;
    }

    async checkRelatedFormatAvailability(): Promise<boolean> {
        let findIndex: number = -1;

        if (this.currentFormat) {
            findIndex = this.relatedFormats.findIndex(format => format.ID === this.currentFormat.ID && format.typeID === this.product.info.typeID);
        }

        if (findIndex === -1) {
            const hasRelatedFormats = this.product?.relatedFormats ? this.product.relatedFormats.length > 0 : false;

            if (!hasRelatedFormats || !this.product.formats.length) {
                this.product.currentFormat = null;
                return true;
            } else {
                // This function needs to be implemented elsewhere in your codebase
                const searchFormat: any = await this.filterFormats(this.product.formats, this.relatedFormats);
                if (searchFormat && searchFormat.length > 0) {
                    return true; // Proceed with logic based on the filtered format array
                }
            }

            return false;
        }

        return false;
    }

    private filterFormats(formats: Array<any>, relatedFormats: Array<any>): Promise<Array<any>> {
        // Implement your filtering logic here, which would depend heavily on the business requirements.
        // This is a placeholder function for demonstration purposes.
        return new Promise((resolve) => resolve([]));
    }
}