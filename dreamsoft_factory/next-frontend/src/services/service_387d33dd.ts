import api from '@/lib/api';

class OrderProcessor {
    async processOrder(order: any): Promise<void> {
        if (order.sumNetPrice !== undefined && order.deliveryNetPrice !== undefined) {
            let tmpNetPrice = this.convertToFloat(order.sumNetPrice);
            let tmpDeliveryNetPrice = this.convertToFloat(order.deliveryNetPrice);

            tmpNetPrice += tmpDeliveryNetPrice;
            console.log(`Processed Net Price: ${tmpNetPrice}`);
        }

        if (order.sumGrossPrice !== undefined && order.deliveryGrossPrice !== undefined) {
            let tmpGrossPrice = this.convertToFloat(order.sumGrossPrice);
            let tmpDeliveryGrossPrice = this.convertToFloat(order.deliveryGrossPrice);

            tmpGrossPrice += tmpDeliveryGrossPrice;
            console.log(`Processed Gross Price: ${tmpGrossPrice}`);
        }
    }

    private convertToFloat(price: any): number {
        if (typeof price === 'string') {
            return parseFloat(price.replace(',', '.'));
        }
        return parseFloat(price);
    }
}