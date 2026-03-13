import api from '@/lib/api';

class ProductHandler {
    private productAddresses: any[] = [];
    private deliveries: any[] = [];
    private price: number = 0;

    async calculateDeliveryPrice(): Promise<void> {
        for (let i = 0; i < this.productAddresses.length; i++) {
            let tmpDeliveryPrice: number = 0;
            const tmp_price: string | undefined = this.productAddresses[i]?.price?.toString();
            
            if (tmp_price) {
                tmpDeliveryPrice += parseFloat(tmp_price.replace(',', '.'));
            }

            const deliveryIdx: number = _.findIndex(this.deliveries, { ID: this.productAddresses[i].deliveryID });
            
            if (deliveryIdx > -1) {
                const tax: number = Number(this.deliveries[deliveryIdx].price.tax / 100) + 1;

                this.price += Number(tmpDeliveryPrice) * tax;
            }
        }

        return Promise.resolve();
    }

    // Example usage
    async exampleUsage(): Promise<void> {
        await api.get('/path/to/api/product-addresses').then(response => {
            this.productAddresses = response.data;
        });

        await api.get('/path/to/api/deliveries').then(response => {
            this.deliveries = response.data;
        });

        await this.calculateDeliveryPrice();
        
        console.log('Total Price:', this.price);
    }
}