import api from '@/lib/api';

class PsConfigOption {
    async removeAllDiscountPrice(optID: string, priceControllerID: string, priceType: string, discountGroupID: string) {
        const removeResource = [
            this.getResource(),
            optID,
            'priceControllers',
            priceControllerID,
            'ps_prices',
            priceType,
            'ps_prices_remove',
            discountGroupID
        ];

        const resource = removeResource.join('/');
        
        try {
            const data = await api.delete(resource);
            if (data.response) {
                return data;
            } else {
                throw new Error('Failed to resolve promise');
            }
        } catch (error) {
            throw error;
        }
    }

    private getResource(): string {
        // Implement this method as necessary
        return ''; 
    }
}