import api from '@/lib/api';

class OrderProcessor {
    private order: any;

    constructor(order: any) {
        this.order = order;
    }

    public async processOrder(): Promise<any> {
        await this.addDeliveryToOrder();
        
        if (this.order.sumPrice !== undefined) {
            const tmpPrice = this.order.sumPrice;
            const tmpDeliveryPrice = this.order.deliveryPrice;

            // Further processing logic with tmpPrice and tmpDeliveryPrice
        }

        return this.order;
    }

    private async addDeliveryToOrder(): Promise<void> {
        if (Array.isArray(this.order.products)) {
            for (const product of this.order.products) {
                if (typeof product.deliveryPrice === 'string') {
                    product.deliveryPrice = product.deliveryPrice.replace(',', '.');
                }
                this.order.deliveryPrice += parseFloat(product.deliveryPrice);
                if (typeof product.deliveryPriceGross === 'string') {
                    product.deliveryPriceGross = product.deliveryPriceGross.replace(',', '.');
                }
                this.order.deliveryGrossPrice += parseFloat(product.deliveryPriceGross);
            }
        }
    }

    public getDeliveryPrice(): number {
        let deliveryPrice = 0;
        
        if (this.order.products) {
            for (const product of this.order.products) {
                if (typeof product.deliveryPrice === 'string') {
                    product.deliveryPrice = product.deliveryPrice.replace(',', '.');
                }
                deliveryPrice += parseFloat(product.deliveryPrice);
            }
        }

        return deliveryPrice;
    }
}

// Usage
async function processOrderExample() {
    const order = { /* initial order data */ };
    const processor = new OrderProcessor(order);

    await processor.processOrder();
}