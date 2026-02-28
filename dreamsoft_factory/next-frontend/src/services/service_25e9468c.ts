import api from '@/lib/api';

class ProductProcessor {
    private resource: string;
    private url: string;

    constructor(resource: string, url: string) {
        this.resource = resource;
        this.url = url;
    }

    async processProduct(selectedProductData: any): Promise<void> {
        const complexProduct = await api.getComplexProduct(this.url);
        
        if (!complexProduct.selectedProduct.data.currentFormat.custom) {
            selectedProductData.newProduct.width = selectedProductData.selectedProduct.data.currentFormat.width;
            selectedProductData.newProduct.height = selectedProductData.selectedProduct.data.currentFormat.height;
        } else {
            selectedProductData.newProduct.width = selectedProductData.selectedProduct.data.currentFormat.customWidth + selectedProductData.selectedProduct.data.currentFormat.slope * 2;
            selectedProductData.newProduct.height = selectedProductData.selectedProduct.data.currentFormat.customHeight + selectedProductData.selectedProduct.data.currentFormat.slope * 2;
        }
    }
}