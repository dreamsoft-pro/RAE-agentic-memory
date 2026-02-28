import api from '@/lib/api';
import { resolve } from 'promise';

class ProductManager {
    private async processAttributes(product: any, oneProduct: any): Promise<boolean> {
        const index = _.findIndex(product.calcProducts, cp => cp.typeID === oneProduct.info.typeID);

        if (index > -1) {
            for (const [attributeIndex, attribute] of Object.entries(product.calcProducts[index].attributes)) {
                if (attribute) {
                    oneProduct.selectedOptions[attribute.attrID] = attribute.optID;
                }
                if (attributeIndex === product.calcProducts[index].attributes.length - 1) {
                    return resolve(true);
                }
            }
        }

        return resolve(false);
    }

    private async setFormats(scope: any, product: any, oneProduct: any): Promise<void> {
        const index = _.findIndex(product.calcProducts, cp => cp.typeID === oneProduct.info.typeID);

        if (index > -1) {
            const indexFormat = _.findIndex(oneProduct.formats, f => f.ID === product.calcProducts[index].formatID);
            
            // You can add further logic here to process the found format index
        }
    }

    public async manageProducts(product: any, oneProduct: any): Promise<void> {
        await this.processAttributes(product, oneProduct).then(result => {
            if (result) {
                return this.setFormats({}, product, oneProduct);
            }
        });
    }
}

// Usage example:
const manager = new ProductManager();
manager.manageProducts(yourProductData, yourOneProductData);