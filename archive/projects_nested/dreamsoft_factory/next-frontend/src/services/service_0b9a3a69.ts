import api from '@/lib/api';
import { useState, useEffect } from 'react';

class ProductController {
    private complexProduct: any;
    private attrID: number;

    constructor(complexProduct: any, attrID: number) {
        this.complexProduct = complexProduct;
        this.attrID = attrID;
    }

    async checkPageLimit() {
        const attrIdx = _.findIndex(this.complexProduct.selectedProduct.data.attributes, { attrID: parseInt(this.attrID) });

        if (attrIdx > -1) {
            const attribute = this.complexProduct.selectedProduct.data.attributes[attrIdx];
            
            let maxPages = attribute.maxPages ?? this.complexProduct.selectedProduct.data.currentPages;

            if (this.complexProduct.selectedProduct.data.attrPages[this.attrID]! > maxPages) {
                Notification.info(`maximum_number_of_pages ${maxPages}`);
                this.complexProduct.selectedProduct.data.attrPages[this.attrID] = maxPages;
                return;
            }
        }
    }
}