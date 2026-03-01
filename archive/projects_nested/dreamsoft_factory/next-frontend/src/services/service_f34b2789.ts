import api from '@/lib/api';

class ComplexProductManager {
    private selectedProduct: any;

    constructor(selectedProduct: any) {
        this.selectedProduct = selectedProduct;
    }

    public async updateCustomFormat(): Promise<void> {
        const format = this.selectedProduct.data.currentFormat;

        if (format.custom) {
            format.customWidth = format.minWidth - format.slope * 2;
            format.customHeight = format.minHeight - format.slope * 2;
        }
    }

    public async changeRelatedFormats(scope: any, oneComplex: any): Promise<void> {
        const result: any[] = [];

        scope.complexProducts[0].selectedProduct.data.currentFormat.relatedFormats.forEach((oneRelatedFormat: any, relatedFormatIndex: number) => {
            const index = this.selectedProduct.data.formats.findIndex(format => format.ID === oneRelatedFormat.formatID);

            if (index > -1) {
                result.push(this.selectedProduct.data.formats[index]);
            }
        });
    }
}