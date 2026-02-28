import axios from 'axios';
import { NextPage } from 'next';

class ProductHelper {
    private static instance: ProductHelper;

    private constructor() {}

    public static getInstance(): ProductHelper {
        if (!ProductHelper.instance) {
            ProductHelper.instance = new ProductHelper();
        }
        return ProductHelper.instance;
    }

    async removeEmptyOptionFromSelected(selectedOptions: string[]): Promise<string[]> {
        // Implementation
        return selectedOptions.filter(option => option.trim() !== '');
    }

    async checkFormatExclusions(productData: any): Promise<boolean> {
        // Implementation
        return true; // Return actual logic
    }

    async removeUnActiveOptions(options: any[]): Promise<any[]> {
        // Implementation
        return options.filter(option => option.isActive);
    }

    prepareProductPromise(productId: string): Promise<any> {
        return axios.get(`https://api.example.com/products/${productId}`).then(response => response.data);
    }

    showSumPrice(products: any[]): number {
        return products.reduce((sum, product) => sum + (product.price || 0), 0);
    }

    showSumGrossPrice(products: any[]): number {
        return products.reduce((sum, product) => sum + (product.grossPrice || 0), 0);
    }
}

export default ProductHelper.getInstance();