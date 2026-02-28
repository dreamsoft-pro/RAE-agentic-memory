import api from '@/lib/api';

class ProductController {
    private exclusions: Record<string, number[]> = {};
    private resource: string;
    private url: string;

    public async processOption(option: { maxPages?: number; minPages?: number }, product: { currentPages?: number; excludedOptions?: number[] }) {
        const attrID = 'attrID'; // Assuming this is the attribute ID you're looking for
        if (product.currentPages !== undefined && option.maxPages !== undefined && Number(option.maxPages) > 0) {

            if (product.currentPages! > option.maxPages) {

                const idx = product.excludedOptions?.indexOf(option.ID);
                if (idx === -1) {
                    this.exclusions[attribute.attrID] = this.exclusions[attribute.attrID] || [];
                    this.exclusions[attribute.attrID].push(option.ID);
                }
            }
        }

        if (product.currentPages !== undefined && option.minPages !== undefined && Number(option.minPages) > 0) {

            if (product.currentPages! < option.minPages) {
                // Handle the condition where min pages is not met
                // Your logic here
            }
        }
    }
}

// Usage example:
const productController = new ProductController();
const product = { currentPages: 5, excludedOptions: [123] };
const option = { ID: '456', maxPages: 10, minPages: 3 };

productController.processOption(option, product).catch(console.error);