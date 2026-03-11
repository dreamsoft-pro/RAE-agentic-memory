// nextjs_services/CalculationService.ts

import api from '@/lib/api';

export default class CalculationService {
    private apiUrl: string;

    constructor() {
        this.apiUrl = '/api/calculations';
    }

    public async calculatePrice(productCode: string, quantity: number): Promise<number> {
        const response = await api.get(`${this.apiUrl}/price`, {
            params: {
                product_code: productCode,
                quantity
            }
        });

        return response.data.price;
    }

    public async updateStock(productCode: string, quantityChange: number): Promise<void> {
        await api.post(`${this.apiUrl}/stock`, {
            product_code: productCode,
            change: quantityChange
        });
    }

    // Example of a complex business logic method
    public async calculateTotalPriceWithDiscounts(cartItems: Array<{product_code: string, quantity: number}>, discountCodes?: string[]): Promise<number> {
        let total = 0;

        for (const item of cartItems) {
            const pricePerItem = await this.calculatePrice(item.product_code, item.quantity);
            total += pricePerItem * item.quantity;
        }

        if (discountCodes && discountCodes.length > 0) {
            // Applying discounts logic here. Assume we have an API endpoint to calculate the final price with applied discounts.
            const response = await api.post(`${this.apiUrl}/apply-discounts`, { cart_items: cartItems, discount_codes: discountCodes });
            total -= response.data.discount_amount;
        }

        return total;
    }
}