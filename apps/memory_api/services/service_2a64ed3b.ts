import api from "@/lib/api";
import { useState } from "react";

class ProductManager {
    private complexProduct: any;
    private minHeight: number;
    private maxWidth: number;

    constructor(complexProduct: any, minHeight: number, maxWidth: number) {
        this.complexProduct = complexProduct;
        this.minHeight = minHeight;
        this.maxWidth = maxWidth;
    }

    async validateDimensions(): Promise<void> {
        const currentFormat = this.complexProduct.selectedProduct.data.currentFormat;

        if (currentFormat.customHeight < this.minHeight) {
            Notification.info(`Value lower than minimum ${this.minHeight}`);
            currentFormat.customHeight = this.minHeight;
        }

        if (currentFormat.customWidth > this.maxWidth) {
            Notification.info(`Value greater than maximum ${this.maxWidth}`);
            currentFormat.customWidth = this.maxWidth;
        }
    }

    // Example of how you can use it within a React component
    static useProductManager(complexProduct: any, minHeight: number, maxWidth: number): void {
        const [manager] = useState(() => new ProductManager(complexProduct, minHeight, maxWidth));

        manager.validateDimensions();
    }
}

// Usage in a Next.js page or component:
/*
const PageComponent = () => {
    const complexProduct = /* some product data */;
    const minHeight = 10;
    const maxWidth = 20;

    // Using the static method to manage and validate dimensions
    ProductManager.useProductManager(complexProduct, minHeight, maxWidth);

    return <div>...</div>;
};
*/