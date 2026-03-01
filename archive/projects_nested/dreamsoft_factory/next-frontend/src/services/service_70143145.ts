import axios from 'axios';

class ProductManager {
    async createNewProduct(product: any): Promise<any> {
        const newProduct: { groupID: string; typeID: string; name: string; formatID: string; width?: number; height?: number } = {};

        newProduct.groupID = product.info.groupID;
        newProduct.typeID = product.info.typeID;
        newProduct.name = product.info.typeName;

        if (!product.currentFormat) {
            console.error('Formats must be assigned!');
            throw new Error('Formats must be assigned!');
        }

        newProduct.formatID = product.currentFormat.ID;

        if (!product.currentFormat.custom) {
            newProduct.width = product.currentFormat.width;
            newProduct.height = product.currentFormat.height;
        } else {
            newProduct.width = product.currentFormat.customWidth + product.currentFormat.slope * 2;
            newProduct.height = product.currentFormat.customHeight + product.currentFormat.slope * 2;
        }

        try {
            const response = await axios.post('your-api-endpoint', newProduct);
            return response.data;
        } catch (error) {
            console.error('Failed to create new product:', error);
            throw error;
        }
    }
}