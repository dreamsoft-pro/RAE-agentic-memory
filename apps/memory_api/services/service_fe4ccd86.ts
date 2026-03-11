import api from "@/lib/api";

class ProductManager {
    product: any;
    sheets: number;

    constructor(product: any, sheets: number) {
        this.product = product;
        this.sheets = sheets;
    }

    private calculateThickness(): number | null {
        let value = 0;
        const keyThickness = Object.keys(this.product.thickness.values);
        if (keyThickness.length === 0 || !this.product.selectedOptions) return null;

        for (let index = 0; index < keyThickness.length; index++) {
            const tmpAttrID = keyThickness[index];
            const one = this.product.thickness.values[tmpAttrID];

            if (Number(one) > 0 && tmpAttrID in this.product.selectedOptions) {
                value += Number(one);
            }
        }

        return this.sheets * value;
    }

    async updateSummary(): Promise<void> {
        // Assuming product.typeID and summaryThickness are available in the class context
        const calculatedThickness = this.calculateThickness();
        
        if (calculatedThickness !== null) {
            this.product.thickness.current = calculatedThickness;
            await api.post('/update-summary', { [this.product.typeID]: calculatedThickness });
        }
    }

    async getMinimumThickness(type: string): Promise<void> {
        // Assuming you need to fetch minimum thickness from the API
        const response = await api.get(`/minimum-thickness/${type}`);
        console.log(response.data);
    }
}

// Usage Example:
const productData = { /* Your product data */ };
const sheetsValue = 10; // Example sheets value

const manager = new ProductManager(productData, sheetsValue);

manager.updateSummary();
manager.getMinimumThickness('example-type');