import api from '@/lib/api';

export default class ProductController {
    private noReload: boolean | undefined;
    private selectedProductData: any;
    private productItem: { amount: number };
    
    constructor() {
        this.noReload = undefined; // or set to true/false based on initialization requirement
        this.selectedProductData = {}; // initialize with actual data
        this.productItem = { amount: 0 }; // initialize with actual amount
    }

    public async getVolumes(selectedProductData: any, amount: number): Promise<void> {
        if (this.noReload === undefined || !this.noReload) {
            await this.fetchAndProcessVolumes(selectedProductData, amount);
        }
    }

    private async fetchAndProcessVolumes(selectedProductData: any, amount: number): Promise<void> {
        // Assuming you want to do some API call or process here
        try {
            const response = await api.get('/some-endpoint');
            console.log('Response data:', response.data);
        } catch (error) {
            console.error('Error fetching volumes:', error);
        }
    }

    public calcProductThickness(product: any): void {
        if (!product || !product.currentPages) return;

        const sheets = product.currentPages / 2;
        console.log(`Calculated sheets for product: ${sheets}`);
        
        // Further processing of sheets can be added here
    }
}