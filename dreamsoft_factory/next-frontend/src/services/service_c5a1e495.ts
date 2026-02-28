import api from '@/lib/api';
import { Deferred } from 'ts deferred'; // Assuming a similar utility library for promises

class CalcSimplifyWidgetService {
    private scope: any;
    private data: any;
    private originalProduct: any;

    async prepareProductPromise(scope: any, newItem: any): Promise<any> {
        this.scope = scope; // Ensure the variable is defined
        this.data = {}; // Initialize necessary variables
        const newItemPrepared = await this.prepareNewItem(newItem);
        if (newItemPrepared) {
            return newItemPrepared;
        }
    }

    private async prepareNewItem(newItem: any): Promise<any> {
        try {
            // Simulate the preparation logic here
            // Example:
            const preparedItem = await api.prepareProduct(newItem); 
            return preparedItem; 
        } catch (error) {
            console.error('Failed to prepare new item', error);
            throw error;
        }
    }

    async selectComplexProduct(scope: any, data: any, originalProduct: any): Promise<any> {
        this.scope = scope;
        this.data = data;
        this.originalProduct = originalProduct;

        const def = new Deferred();

        let emptyProducts = 0; // Ensure the variable is defined

        this.scope.complexProducts = data.complex || []; // Handle potential undefined case

        for (let complexIndex in this.scope.complexProducts) {
            const oneComplex = this.scope.complexProducts[complexIndex];
            for (let productIndex in oneComplex.products) {
                await this.initSelectedProduct(oneComplex, oneComplex.products[productIndex]);
                const originalCalcProduct = this.findOriginalCalcProduct(oneComplex);
                if (originalCalcProduct) {
                    await this.addSelectedProductFormats(oneComplex, data.formats?.[oneComplex.selectedProduct.typeID] || []);
                }
            }
        }

        def.resolve(this.scope); // Resolve the promise with scope or any relevant value

        return def.promise;
    }

    private async initSelectedProduct(complex: any, product: any): Promise<void> {
        // Implement initialization logic here
        complex.selectedProduct = { ...product }; // Example of setting selected product
    }

    private findOriginalCalcProduct(complex: any): any {
        const originalCalcProduct = this.originalProduct.calcProducts?.find(
            (calcProduct) => calcProduct.typeID === complex.selectedProduct.typeID
        );
        return originalCalcProduct;
    }

    private async addSelectedProductFormats(complex: any, formats: any[]): Promise<void> {
        // Implement adding selected product formats logic here
        // Example:
        complex.formats = formats.filter((format) => format.active); 
    }
}