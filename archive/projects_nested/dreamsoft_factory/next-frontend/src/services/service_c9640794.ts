import api from "@/lib/api";
import * as _ from "lodash";

interface Scope {
    selectDefaultOptions(productData: any): void;
    complexProducts: Array<any>;
    complexIndex: number;
}

class ProductHandler {

    private scope: Scope;

    constructor(scope: Scope) {
        this.scope = scope;
    }

    async setExclusionsAsync(productData: any, complexIndex?: number): Promise<boolean> {
        let exclusionEnd = await this.getExclusionStatus();

        if (exclusionEnd) {
            this.scope.selectDefaultOptions(productData);

            if ((this.scope.complexProducts.length - 1) === (complexIndex ?? this.scope.complexIndex)) {
                return true;
            }
        }

        return false;
    }

    private async getExclusionStatus(): Promise<boolean> {
        // Simulate fetching exclusion status
        // Replace with actual API call if needed
        const response = await api.get('/exclusions');
        return response.data.exclusionEnd ?? false;  // Assume response has a field 'exclusionEnd'
    }

    setOptions(product: any, oneProduct: any): void {
        let index = _.findIndex(product.calcProducts, { typeID: oneProduct.info.typeID });

        // Assuming you want to resolve a promise in this method
        const def = Promise.resolve();
        def.then(() => {
            // Handle your logic here
        });
    }
}