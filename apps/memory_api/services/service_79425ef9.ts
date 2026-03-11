import { findIndex } from 'lodash';
import api from '@/lib/api';

class ComplexProductManager {
    private complexProduct: any;
    private attrID: number;
    private direct: number;

    constructor(complexProduct: any, attrID: number, direct: number) {
        this.complexProduct = complexProduct;
        this.attrID = attrID;
        this.direct = direct;
    }

    public async releaseSpinner(): Promise<void> {
        if (this.complexProduct.selectedProduct.data.attrPages[this.attrID] <= 0 && this.direct === 0) {
            return;
        }

        const attrIdx: number | -1 = findIndex(this.complexProduct.selectedProduct.data.attributes, { attrID: parseInt(String(this.attrID)) });

        if (attrIdx > -1) {
            const attribute: any = this.complexProduct.selectedProduct.data.attributes[attrIdx];

            const step: number = attribute.step;

            // If you have an async function here that needs to be awaited:
            // await someAsyncFunction();
        }
    }

    public static formatChangedCheck(formatChange: boolean): Promise<void> {
        return new Promise((resolve) => {
            if (!formatChange) {
                resolve();
            } else {
                console.log('Format zmieniony ale czemu tu doszło :o');
            }
        });
    }
}