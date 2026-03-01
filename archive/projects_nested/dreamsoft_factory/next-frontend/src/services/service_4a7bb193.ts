import api from '@/lib/api';

class ProductEditorComponent {
    private complexProducts: any[] = [];
    private calculation: { amount: number } = { amount: 0 };
    private editorUrl: string | null = null;

    prepareUrl() {
        if (this.complexProducts.length === 1 && this.calculation.amount > 0) {
            this.getPreparedProduct(this.complexProducts[0], this.calculation.amount).then((preparedProduct) => {
                const returnedProduct = preparedProduct.products[0];

                // Ensure $config.EDITOR_URL is defined before use
                if (typeof ($config as any)?.EDITOR_URL !== 'string') {
                    throw new Error('Configuration EDITOR_URL is missing or incorrect');
                }

                this.editorUrl = `${($config as any).EDITOR_URL}?typeID=${returnedProduct.typeID}&formatID=${returnedProduct.formatID}&pages=${returnedProduct.pages}`;
            });
        }
    }

    private async getPreparedProduct(product: any, amount: number): Promise<{ products: any[] }> {
        // Assuming 'prepareProduct' is a function that prepares the product and returns a promise
        return await api.prepareProduct(product, amount);
    }
}