import api from '@/lib/api';

interface SelectedProductData {
    thickness: {
        min?: number | null;
        max?: number | null;
        minAttr?: number | null;
        maxAttr?: number | null;
    };
}

export default class ProductService {
    private selectedProductData: SelectedProductData;

    constructor(selectedProductData: SelectedProductData) {
        this.selectedProductData = selectedProductData;
    }

    async updateThicknessAttributes(attrID: number): Promise<void> {
        // Ensure all variables are defined before use
        if (this.selectedProductData.thickness.maxAttr === attrID) {
            this.selectedProductData.thickness.max = null;
            this.selectedProductData.thickness.maxAttr = null;
        }

        const itemsResponse = await api.get('/items');  // Replace '/items' with actual API endpoint
        const items: { minThickness?: number; maxThickness?: number; sizePage?: number }[] = itemsResponse.data;

        for (const item of items) {
            if (
                Number(item.minThickness ?? 0) > 0 &&
                (Number(item.minThickness ?? 0) > (this.selectedProductData.thickness.min ?? -Infinity) ||
                item.minThickness === null)
            ) {
                this.selectedProductData.thickness.min = item.minThickness;
                this.selectedProductData.thickness.minAttr = attrID;
            }
        }
    }

    // Add other methods as needed
}