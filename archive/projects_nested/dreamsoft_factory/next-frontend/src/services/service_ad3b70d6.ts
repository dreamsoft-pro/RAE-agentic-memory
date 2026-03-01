import api from '@/lib/api';

class ComplexProductController {
    private stopSelectAttr: NodeJS.Timeout | undefined;

    async adjustAttributePage(complexProduct: any, attrID: number, step: number, direct: boolean) {
        if (direct) {
            complexProduct.selectedProduct.data.attrPages[attrID] += step;
        } else {
            complexProduct.selectedProduct.data.attrPages[attrID] -= step;
        }

        await this.selectAttrPages(complexProduct, attrID);
    }

    private async selectAttrPages(complexProduct: any, attrID: number) {
        if (this.stopSelectAttr !== undefined) {
            clearTimeout(this.stopSelectAttr as NodeJS.Timeout);
        }

        const timeoutPromise = new Promise<void>((resolve) => {
            this.stopSelectAttr = setTimeout(() => {
                resolve();
            }, 0); // Assuming immediate resolution for simplicity
        });

        await timeoutPromise;

        if (complexProduct.selectedProduct.data.attrPages[attrID] <= 0) {
            complexProduct.selectedProduct.data.attrPages[attrID] = 0;
        }
    }
}