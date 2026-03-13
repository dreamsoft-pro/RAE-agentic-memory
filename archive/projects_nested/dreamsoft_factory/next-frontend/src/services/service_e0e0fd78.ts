import api from '@/lib/api';

async function filterFormats(formats: string[], relatedFormats: string[]): Promise<string[]> {
    // Implement the logic to filter formats here
    return formats;
}

function selectDefaultFormats(complexProducts: any[]): void {
    const q = {};
    for (let i = 1; i < complexProducts.length; i++) {
        const oneProduct = complexProducts[i];
        if (!oneProduct.selectedProduct) {
            continue;
        }
        const product = oneProduct.selectedProduct.data;

        const currentFormat = product.currentFormat;
    }
}