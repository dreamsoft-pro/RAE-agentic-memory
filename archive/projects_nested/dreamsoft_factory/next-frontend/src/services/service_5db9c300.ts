import api from '@/lib/api';
import { useState, useEffect } from 'react';

interface ComplexProduct {
    // Define properties here if needed
}

interface OptionMap {
    [key: number]: string[];
}

interface Item {
    ID: number;
    // Other item properties as necessary
}

class ProductHelper {
    private complexProducts: ComplexProduct[] = [];
    private index: number;

    constructor(complexProducts: ComplexProduct[], index: number) {
        this.complexProducts = complexProducts;
        this.index = index;
    }

    async processComplexProduct(): Promise<void> {
        const newItem = await this.getNewItem();
        
        // Simulate the timeout using setTimeout in an async function
        if ((this.complexProducts.length - 1) === this.index) {
            return new Promise(resolve => setTimeout(() => resolve(newItem), 1000));
        }

        throw new Error('Not last item');
    }

    private async getNewItem(): Promise<Item> {
        // Define how you would get the new item
        const product = await api.getProduct(); // Example API call, adjust as necessary

        return this.getAttributeFromOption(product);
    }

    private async getAttributeFromOption(product: ComplexProduct): Promise<number> {
        const def = Promise.resolve<number>();

        for (const [attrID, options] of Object.entries(product.optionMap)) {
            if (options.includes('some_option_id')) { // Replace 'some_option_id' with actual logic
                return parseInt(attrID);
            }
        }

        throw new Error('Attribute ID not found');
    }

    filterFormats(input: Item[], ids: { ID: number }[]): Item[] {
        const result: Item[] = [];

        for (const item of input) {
            if (ids.some(id => id.ID === item.ID)) {
                result.push(item);
            }
        }

        return result;
    }
}

// Example usage
export default function YourComponent() {
    const [complexProducts, setComplexProducts] = useState<ComplexProduct[]>([]);
    const index: number = 0; // Define your index here

    useEffect(() => {
        const productHelper = new ProductHelper(complexProducts, index);
        
        async function runProcess() {
            try {
                await productHelper.processComplexProduct();
            } catch (error) {
                console.error(error.message);
            }
        }

        runProcess();

        // For demonstration purposes only. Typically you would fetch complex products in useEffect.
    }, [complexProducts]);

    return (
        <div>
            {/* Render your component here */}
        </div>
    );
}