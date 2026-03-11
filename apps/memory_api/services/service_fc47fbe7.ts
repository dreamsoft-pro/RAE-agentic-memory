import api from '@/lib/api';
import { useState, useEffect } from 'react';

class ComplexProductPageController {
    private maxPages: number | null = null;
    private complexProduct: any; // Replace `any` with the actual type when available
    private attribute: any; // Replace `any` with the actual type when available

    constructor(complexProduct: any, attribute: any) {
        this.complexProduct = complexProduct;
        this.attribute = attribute;
        this.maxPages = attribute.maxPages ?? null;

        if (this.maxPages === null) {
            this.maxPages = this.complexProduct.selectedProduct.data.currentPages;
        }
    }

    async handlePageChange(attrID: number, step: number, direct: number): Promise<void> {
        const minPages = this.attribute.minPages;

        if ((this.complexProduct.selectedProduct.data.attrPages[attrID] + step) > this.maxPages && direct === 1) {
            Notification.info(`maximum_number_of_pages ${this.maxPages}`);
            return;
        }

        if ((this.complexProduct.selectedProduct.data.attrPages[attrID] - step) < minPages && direct === 0) {
            Notification.info(`minimum_number_of_pages ${minPages}`);
            return;
        }
    }
}