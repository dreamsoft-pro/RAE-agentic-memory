import api from "@/lib/api";
import _ from "lodash";

class ComplexManager {
    private scope: any;
    private oneComplex: any;

    constructor(scope: any, oneComplex: any) {
        this.scope = scope;
        this.oneComplex = oneComplex;
    }

    public async filterRelatedFormats(): Promise<void> {
        await this.changeRelatedFormats();

        const result = await api.getRelatedFormats(); // Replace with actual API call or logic

        if (this.oneComplex.selectedProduct && this.oneComplex.selectedProduct.data) {
            this.oneComplex.selectedProduct.data.relatedFormats = _.clone(result);

            const index = _.findIndex(this.oneComplex.selectedProduct.data.relatedFormats, { ID: this.oneComplex.selectedProduct.data.currentFormat.ID });

            if (index === -1) {
                this.oneComplex.selectedProduct.data.currentFormat = _.first(this.oneComplex.selectedProduct.data.relatedFormats);
            }
        }

        // Resolve promise conditionally
        if ((this.scope.complexProducts.length - 1) === this.scope.complexIndex &&
            (this.oneComplex.products.length - 1) === this.scope.productIndex) {
            return Promise.resolve(true);
        } else {
            return Promise.reject(false); // Adjust as necessary
        }
    }

    private async changeRelatedFormats(): Promise<any> {
        // Implement business logic or API call here
        const result = await api.changeRelatedFormat(); // Replace with actual API call or logic

        this.oneComplex.selectedProduct.data.relatedFormats = result;

        return result;
    }
}