import api from '@/lib/api';
import _ from 'lodash';

class ProductHandler {
    private scope: any;

    constructor(scope: any) {
        this.scope = scope;
    }

    public async selectDefaultFormats(): Promise<void> {
        let def: Promise<void>;
        let productData: any;

        _.each(this.scope.complexProducts, async (oneProduct, complexIndex) => {

            if (!oneProduct.selectedProduct) {
                return true;
            }

            if (complexIndex === 0) {
                await this.setRangePages(oneProduct.selectedProduct.data);
            }

            productData = oneProduct.selectedProduct.data;

            if (!productData.currentFormat) {
                productData.currentFormat = _.first(productData.formats);
            }

            if (complexIndex > 0) {
                await this.filterRelatedFormats(this.scope, oneProduct);
            }

            try {
                await this.checkFormatExclusions(productData);
            } catch (error) {
                console.error('Error checking format exclusions:', error);
            }
        });
    }

    private async setRangePages(data: any): Promise<void> {
        for (const attribute of data.attributes) {
            await api.setRangePages(data, attribute.attrID); // Assuming `api` has a method `setRangePages`
        }
    }

    private async filterRelatedFormats(scope: any, oneProduct: any): Promise<void> {
        // Implement the business logic here
    }

    private async checkFormatExclusions(productData: any): Promise<void> {
        try {
            await api.checkFormatExclusions(productData); // Assuming `api` has a method `checkFormatExclusions`
        } catch (error) {
            console.error('Error checking format exclusions:', error);
        }
    }
}