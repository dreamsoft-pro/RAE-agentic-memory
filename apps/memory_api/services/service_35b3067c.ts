import api from '@/lib/api';
import _ from 'lodash';

class ProductHandler {
    async handleComplexProducts(scope: any): Promise<void> {
        const newItem = { products: [] };
        
        for (const [index, complexProduct] of Object.entries(scope.complexProducts)) {
            if (!complexProduct.selectedProduct || !complexProduct.selectedProduct.data) {
                console.error('Selected product data is missing in complex product.');
                continue;
            }

            const selectedProductData = complexProduct.selectedProduct.data.info;

            const newProduct: any = {
                groupID: selectedProductData.groupID,
                typeID: selectedProductData.typeID,
                name: selectedProductData.typeName
            };

            if (!selectedProductData.currentFormat || !selectedProductData.currentFormat.ID) {
                console.error('Formats must be assigned!');
                continue;
            }

            newProduct.formatID = selectedProductData.currentFormat.ID;

            newItem.products.push(newProduct);
        }
    }
}

// Usage example:
const handler = new ProductHandler();
handler.handleComplexProducts(scope).then(() => {
    // Handle the completion or error as necessary
}).catch((error) => {
    console.error('Error handling complex products:', error);
});