import api from '@/lib/api';

class ProductHelper {
    async processComplexProduct(complexProduct: any, originalCalcProduct?: any): Promise<void> {
        if (originalCalcProduct?.pages) {
            complexProduct.selectedProduct.data.currentPages = originalCalcProduct.pages;
        } else if (_.first(complexProduct.selectedProduct.data.pages)?.minPages) {
            complexProduct.selectedProduct.data.currentPages = _.first(complexProduct.selectedProduct.data.pages).minPages;
        } else {
            complexProduct.selectedProduct.data.currentPages = 2;
        }
    }

    async addSelectProductAttrPages(complexProduct: any, originalProduct: any): Promise<void> {
        const calcProduct = _.find(originalProduct.calcProducts, { typeID: complexProduct.selectedProduct.typeID });
        if (calcProduct) {
            _.each(calcProduct.attributes, attribute => {
                if (attribute.attrPages > 0) {
                    complexProduct.selectedProduct.data.attrPages[attribute.attrID] = attribute.attrPages;
                }
            });
        }
    }
}