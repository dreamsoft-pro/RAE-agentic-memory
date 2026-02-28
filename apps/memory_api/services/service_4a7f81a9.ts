import api from '@/lib/api';
import _ from 'lodash';

class ProductHelper {

    async getMaximumThickness(product: any): Promise<number> {
        if (!_.keys(product.thickness.values).length || !product.thickness.max) {
            return product.pages[0].maxPages || 9999999;
        }

        let value = 0;

        await _.each(_.values(product.thickness.values), async (one: number) => {
            if (Number(one) > 0) {
                value += one;
            }
        });

        const sheets = product.thickness.max / value;
        const pages = Math.floor(sheets) * 2;
        const doublePage = !!product.pages[0].doublePage;

        return doublePage ? pages * 2 : pages;
    }

}

export default ProductHelper;