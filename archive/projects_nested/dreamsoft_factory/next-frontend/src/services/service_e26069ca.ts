import api from '@/lib/api';
import _ from 'lodash';

class ProductManager {
    async addSelectProductCustomFormat(complexProduct: any, attributesData: any[]): Promise<void> {
        const customFormatIndex = _.findIndex(attributesData, { attrID: -1 });
        if (customFormatIndex > -1) {
            complexProduct.selectedProduct.data.customFormatInfo = attributesData[customFormatIndex];
            attributesData.splice(1, customFormatIndex);
        }
    }

    async addSelectProductCustomPageInfo(complexProduct: any, attributesData: any[]): Promise<void> {
        const customPageIndex = _.findIndex(attributesData, { attrID: -2 });
        if (customPageIndex > -1) {
            complexProduct.selectedProduct.data.customPageInfo = attributesData[customPageIndex];
            attributesData.splice(1, customPageIndex);
        }
    }
}