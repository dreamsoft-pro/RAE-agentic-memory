import axios from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';

interface Product {
    currentFormat?: string;
    attributes: Array<{ options?: any[] }>;
}

export class CalcSimplifyWidgetService {
    private checkFormatExclusions = async (product: Product, format: string): Promise<boolean> => {
        if (!product.currentFormat) {
            throw new Error('no product.currentFormat');
        }
        product.formatExcluded = [];

        for (const [attributeIndex, attribute] of Object.entries(product.attributes)) {
            if (!attribute.options && parseInt(attributeIndex as any) === product.attributes.length - 1) {
                return true;
            }

            for (const option of attribute.options ?? []) {
                // Your logic here
            }
        }

        throw new Error('Unexpected error in checkFormatExclusions');
    };

    public async runCheck(product: Product, format: string): Promise<void> {
        try {
            const result = await this.checkFormatExclusions(product, format);
            console.log(result);
        } catch (error) {
            console.error(error.message);
        }
    }
}

// Usage
const calcSimplifyWidgetService = new CalcSimplifyWidgetService();
calcSimplifyWidgetService.runCheck({ currentFormat: 'someFormat', attributes: [{ options: ['option1'] }, { options: undefined }] }, 'format');