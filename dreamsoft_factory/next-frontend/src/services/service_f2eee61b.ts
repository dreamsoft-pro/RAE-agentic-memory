import api from '@/lib/api';

class ProductSelectionService {
    private selectedProductData: any = {};
    private productItem: any = {};

    selectDefaultOptions(data: any) {
        this.selectedProductData = data;
        if (!this.checkItemExistence()) {
            this.setSelectedProperties();
        }
    }

    private async checkItemExistence(): Promise<boolean> {
        // Assuming you have a method to check item existence
        const response = await api.get('/some-endpoint');
        return Boolean(response.data.itemExists);
    }

    private setSelectedProperties() {
        if (this.selectedProductData.info) {
            this.selectedProductData.typeID = this.selectedProductData.info.typeID;
            this.selectedProductData.groupID = this.selectedProductData.info.groupID;
        }
        this.selectedProductData.taxID = this.productItem.taxID || 0; // Defaulting to 0 if taxID is falsy
        this.selectedProductData.name = this.productItem.name || '';
        this.selectedProductData.realizationTimeID = this.productItem.realizationTimeID || 0;
    }
}

// Usage example:
const productService = new ProductSelectionService();
productService.selectDefaultOptions({
    info: {
        typeID: 1,
        groupID: 2
    },
});